#!/usr/bin/env python3
"""
gmail-coverage
A playful Rich CLI for measuring how much incoming Gmail traffic is covered
by deliberate sender/domain routing rules, then fixing the highest-impact gap.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import time
import random
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date, timedelta
from email.utils import parseaddr
from pathlib import Path
from typing import Iterable

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.prompt import Confirm, IntPrompt, Prompt
from rich.table import Table
from rich.text import Text

APP_NAME = "gmail-coverage"
CONFIG_DIR = Path.home() / ".gmail-coverage"
TOKEN_FILE = CONFIG_DIR / "token.json"
CLIENT_FILE = CONFIG_DIR / "credentials.json"
SETTINGS_FILE = CONFIG_DIR / "settings.json"
CACHE_FILE = CONFIG_DIR / "message_cache.json"

# Gmail currently charges 20 quota units for messages.get and allows
# 6,000 units/minute/user. 0.24s/request ~= 250 reads/minute, leaving
# useful headroom for labels, filters and interactive rule creation.
MESSAGE_GET_INTERVAL = 0.24
MAX_QUOTA_RETRIES = 7

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.settings.basic",
]

console = Console()


@dataclass
class MessageRow:
    id: str
    sender: str
    domain: str
    label_ids: list[str]


@dataclass
class Coverage:
    total: int
    covered: int
    by_domain: Counter
    uncovered_by_domain: Counter
    uncovered_by_sender: Counter
    domain_senders: dict[str, Counter]
    domain_labels: dict[str, Counter]

    @property
    def pct(self) -> float:
        return (self.covered / self.total * 100.0) if self.total else 100.0


def banner() -> None:
    art = r"""
   ____                 _ _    ____                                
  / ___|_ __ ___   __ _(_) |  / ___|_____   _____ _ __ __ _  __ _  ___
 | |  _| '_ ` _ \ / _` | | | | |   / _ \ \ / / _ \ '__/ _` |/ _` |/ _ \
 | |_| | | | | | | (_| | | | | |__| (_) \ V /  __/ | | (_| | (_| |  __/
  \____|_| |_| |_|\__,_|_|_|  \____\___/ \_/ \___|_|  \__,_|\__, |\___|
                                                             |___/
"""
    console.print(Panel(Text(art, style="bold cyan"), subtitle="How much of your inbox has a plan?", border_style="cyan"))


def ensure_config_dir() -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    try:
        os.chmod(CONFIG_DIR, 0o700)
    except OSError:
        pass



def is_quota_error(exc: HttpError) -> bool:
    status = getattr(getattr(exc, "resp", None), "status", None)
    if status not in (403, 429):
        return False
    body = str(exc).lower()
    return any(
        reason in body
        for reason in (
            "ratelimitexceeded",
            "userratelimitexceeded",
            "quota exceeded",
            "quotaexceeded",
            "resource_exhausted",
        )
    )


def execute_with_backoff(request, description: str = "Gmail request"):
    """Execute a Gmail API request, automatically backing off on quota errors."""
    for attempt in range(MAX_QUOTA_RETRIES + 1):
        try:
            return request.execute()
        except HttpError as exc:
            if not is_quota_error(exc) or attempt >= MAX_QUOTA_RETRIES:
                raise

            retry_after = 0.0
            try:
                retry_after = float(exc.resp.get("retry-after", 0) or 0)
            except (TypeError, ValueError, AttributeError):
                retry_after = 0.0

            exponential = min((2 ** attempt) + random.random(), 64.0)
            wait = max(retry_after, exponential)

            console.print(
                Panel(
                    f"[yellow bold]Gmail asked us to slow down.[/yellow bold]\n\n"
                    f"{description}\n"
                    f"Retry {attempt + 1}/{MAX_QUOTA_RETRIES} in [bold]{wait:.1f}s[/bold].\n\n"
                    "[dim]Authentication is fine; this is a temporary API quota limit.[/dim]",
                    title="⏳ Quota cooldown",
                    border_style="yellow",
                )
            )
            time.sleep(wait)


def load_message_cache() -> dict[str, dict]:
    ensure_config_dir()
    if not CACHE_FILE.exists():
        return {}
    try:
        data = json.loads(CACHE_FILE.read_text())
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def save_message_cache(cache: dict[str, dict]) -> None:
    ensure_config_dir()
    tmp = CACHE_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(cache, separators=(",", ":")))
    tmp.replace(CACHE_FILE)
    try:
        os.chmod(CACHE_FILE, 0o600)
    except OSError:
        pass

def first_run_help() -> Path:
    ensure_config_dir()
    console.print(
        Panel(
            "[bold]First run: connect Gmail[/bold]\n\n"
            "This tool needs a Google OAuth [bold]Desktop app[/bold] credential.\n\n"
            "1. Open Google Cloud Console\n"
            "2. Create/select a project\n"
            "3. Enable the Gmail API\n"
            "4. Configure the Google Auth consent screen\n"
            "5. Create an OAuth Client ID with application type [bold]Desktop app[/bold]\n"
            "6. Download the JSON credentials file\n\n"
            "The tool will copy that file into [cyan]~/.gmail-coverage/credentials.json[/cyan].",
            title="🔐 Authentication setup",
            border_style="yellow",
        )
    )
    path = Path(Prompt.ask("Path to the downloaded credentials JSON", default="./credentials.json")).expanduser()
    if not path.exists():
        console.print(f"[red]Could not find:[/red] {path}")
        raise SystemExit(2)
    shutil.copy2(path, CLIENT_FILE)
    try:
        os.chmod(CLIENT_FILE, 0o600)
    except OSError:
        pass
    console.print(f"[green]✓[/green] Saved credentials to {CLIENT_FILE}")
    return CLIENT_FILE


def get_credentials() -> Credentials:
    ensure_config_dir()
    creds = None

    if TOKEN_FILE.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
        except Exception:
            console.print("[yellow]⚠ Existing token could not be loaded; re-authentication is needed.[/yellow]")

    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
        except Exception:
            creds = None

    if not creds or not creds.valid:
        if not CLIENT_FILE.exists():
            first_run_help()

        console.print("\n[bold cyan]Opening your browser to authorise Gmail…[/bold cyan]")
        console.print("[dim]The refresh token is stored locally in ~/.gmail-coverage/token.json.[/dim]\n")
        flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_FILE), SCOPES)
        creds = flow.run_local_server(port=0)

        TOKEN_FILE.write_text(creds.to_json())
        try:
            os.chmod(TOKEN_FILE, 0o600)
        except OSError:
            pass
        console.print("[green]✓ Gmail authorised[/green]")
    else:
        console.print("[green]✓ Using saved Gmail authorisation[/green]")

    return creds


def period_bounds(period: str) -> tuple[date, date, str]:
    today = date.today()

    if period == "today":
        start, end = today, today + timedelta(days=1)
        label = "today"
    elif period == "week":
        start = today - timedelta(days=today.weekday())
        end = today + timedelta(days=1)
        label = "this week"
    elif period == "month":
        start = today.replace(day=1)
        end = today + timedelta(days=1)
        label = "this month"
    elif period == "quarter":
        q_month = ((today.month - 1) // 3) * 3 + 1
        start = date(today.year, q_month, 1)
        end = today + timedelta(days=1)
        label = "this quarter"
    elif period == "last-quarter":
        q_month = ((today.month - 1) // 3) * 3 + 1
        this_q = date(today.year, q_month, 1)
        prev_end = this_q
        prev_last = this_q - timedelta(days=1)
        prev_q_month = ((prev_last.month - 1) // 3) * 3 + 1
        start = date(prev_last.year, prev_q_month, 1)
        end = prev_end
        label = "last quarter"
    elif period == "year":
        start = date(today.year, 1, 1)
        end = today + timedelta(days=1)
        label = "this year"
    else:
        raise ValueError(period)

    return start, end, label


def gmail_date(d: date) -> str:
    return d.strftime("%Y/%m/%d")


def list_message_ids(service, query: str) -> list[str]:
    ids: list[str] = []
    token = None
    while True:
        resp = execute_with_backoff(
            service.users().messages().list(
                userId="me", q=query, pageToken=token, maxResults=500
            ),
            "Listing messages",
        )
        ids.extend(m["id"] for m in resp.get("messages", []))
        token = resp.get("nextPageToken")
        if not token:
            break
    return ids

def fetch_messages(service, ids: list[str]) -> list[MessageRow]:
    cache = load_message_cache()
    rows: list[MessageRow] = []
    uncached = [message_id for message_id in ids if message_id not in cache]

    cache_hits = len(ids) - len(uncached)
    if cache_hits:
        console.print(
            f"[dim]Cache: {cache_hits:,} message headers reused · "
            f"{len(uncached):,} need Gmail API reads[/dim]"
        )

    for message_id in ids:
        cached = cache.get(message_id)
        if not cached:
            continue
        sender = cached.get("sender", "")
        domain = cached.get("domain", "")
        if sender and domain:
            rows.append(
                MessageRow(
                    id=message_id,
                    sender=sender,
                    domain=domain,
                    label_ids=cached.get("label_ids", []),
                )
            )

    if not uncached:
        return rows

    console.print(
        Panel(
            f"{len(uncached):,} uncached message headers need reading.\n"
            f"The scanner is paced at about [bold]{round(60 / MESSAGE_GET_INTERVAL):,} reads/minute[/bold] "
            "to stay below Gmail's per-user quota.\n\n"
            "[dim]Future scans reuse these cached headers and should be much faster.[/dim]",
            title="🐢 Quota-safe scan",
            border_style="cyan",
        )
    )

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Reading Gmail headers…", total=len(uncached))
        last_request_started = 0.0
        dirty = 0

        for message_id in uncached:
            elapsed = time.monotonic() - last_request_started
            if last_request_started and elapsed < MESSAGE_GET_INTERVAL:
                time.sleep(MESSAGE_GET_INTERVAL - elapsed)

            last_request_started = time.monotonic()
            response = execute_with_backoff(
                service.users().messages().get(
                    userId="me",
                    id=message_id,
                    format="metadata",
                    metadataHeaders=["From"],
                ),
                f"Reading message header {progress.tasks[task].completed + 1:,}/{len(uncached):,}",
            )

            headers = {
                h["name"].lower(): h["value"]
                for h in response.get("payload", {}).get("headers", [])
            }
            _, sender = parseaddr(headers.get("from", ""))
            sender = sender.lower().strip()

            if sender and "@" in sender:
                domain = sender.rsplit("@", 1)[1].lower()
                label_ids = response.get("labelIds", [])
                row = MessageRow(
                    id=response["id"],
                    sender=sender,
                    domain=domain,
                    label_ids=label_ids,
                )
                rows.append(row)
                cache[message_id] = {
                    "sender": sender,
                    "domain": domain,
                    "label_ids": label_ids,
                }
                dirty += 1

            progress.advance(task)

            # Persist periodically, so an interrupted large first scan keeps its work.
            if dirty >= 50:
                save_message_cache(cache)
                dirty = 0

        if dirty:
            save_message_cache(cache)

    return rows

def normalise_from(value: str) -> tuple[str | None, str | None]:
    """Return (sender, domain) from a simple Gmail filter 'from' criterion."""
    if not value:
        return None, None
    _, addr = parseaddr(value)
    candidate = (addr or value).strip().lower()

    if candidate.startswith("@"):
        return None, candidate[1:]
    if candidate.startswith("*@"):
        return None, candidate[2:]
    if "@" in candidate and " " not in candidate:
        return candidate, candidate.rsplit("@", 1)[1]
    return None, None


DOMAIN_QUERY_PATTERNS = [
    re.compile(r"""from:\(?["']?@([a-z0-9.-]+\.[a-z]{2,})["']?\)?""", re.I),
    re.compile(r"""from:\(?["']?\*@([a-z0-9.-]+\.[a-z]{2,})["']?\)?""", re.I),
]


def rule_index(filters: list[dict]) -> tuple[set[str], set[str]]:
    senders: set[str] = set()
    domains: set[str] = set()

    for f in filters:
        criteria = f.get("criteria", {})
        sender, domain = normalise_from(criteria.get("from", ""))
        if sender:
            senders.add(sender)
        elif domain and criteria.get("from", "").strip().startswith(("@", "*@")):
            domains.add(domain)

        query = criteria.get("query", "")
        for pattern in DOMAIN_QUERY_PATTERNS:
            for match in pattern.findall(query):
                domains.add(match.lower())

        # Also recognise our explicit marker style: from:(*@example.org)
        m = re.findall(r"\*@([a-z0-9.-]+\.[a-z]{2,})", query, flags=re.I)
        domains.update(x.lower() for x in m)

    return senders, domains


def analyse(rows: list[MessageRow], filters: list[dict], user_label_ids: set[str]) -> Coverage:
    rule_senders, rule_domains = rule_index(filters)
    covered = 0
    by_domain = Counter()
    uncovered_by_domain = Counter()
    uncovered_by_sender = Counter()
    domain_senders = defaultdict(Counter)
    domain_labels = defaultdict(Counter)

    for row in rows:
        by_domain[row.domain] += 1
        domain_senders[row.domain][row.sender] += 1

        is_covered = row.sender in rule_senders or row.domain in rule_domains
        if is_covered:
            covered += 1
            continue

        uncovered_by_domain[row.domain] += 1
        uncovered_by_sender[row.sender] += 1
        for label_id in row.label_ids:
            if label_id in user_label_ids:
                domain_labels[row.domain][label_id] += 1

    return Coverage(
        total=len(rows),
        covered=covered,
        by_domain=by_domain,
        uncovered_by_domain=uncovered_by_domain,
        uncovered_by_sender=uncovered_by_sender,
        domain_senders=dict(domain_senders),
        domain_labels=dict(domain_labels),
    )


def bar(pct: float, width: int = 36) -> str:
    full = round(width * pct / 100)
    return "█" * full + "░" * (width - full)


def show_summary(cov: Coverage, period_label: str, label_names: dict[str, str]) -> None:
    uncovered = cov.total - cov.covered
    console.print()
    console.print(
        Panel(
            f"[bold]{bar(cov.pct)}[/bold]  [bold cyan]{cov.pct:5.1f}%[/bold cyan]\n\n"
            f"[green]✓ PASS[/green]  {cov.covered:,} messages covered\n"
            f"[red]✗ FAIL[/red]  {uncovered:,} messages have no sender/domain rule\n"
            f"[dim]{cov.total:,} messages analysed · {len(cov.by_domain):,} domains[/dim]",
            title=f"📨 Rule coverage · {period_label}",
            border_style="cyan",
        )
    )

    table = Table(
        title="🏆 Highest-impact uncovered traffic",
        box=box.ROUNDED,
        show_lines=False,
    )
    table.add_column("#", justify="right", style="dim")
    table.add_column("Domain", style="bold")
    table.add_column("Emails", justify="right")
    table.add_column("% mail", justify="right")
    table.add_column("Senders", justify="right")
    table.add_column("Potential gain", justify="right", style="green")
    table.add_column("Existing label signal", overflow="fold")

    for i, (domain, count) in enumerate(cov.uncovered_by_domain.most_common(12), 1):
        share = count / cov.total * 100 if cov.total else 0
        senders = len(cov.domain_senders.get(domain, {}))
        label_signal = "—"
        if cov.domain_labels.get(domain):
            lid, n = cov.domain_labels[domain].most_common(1)[0]
            label_signal = f"{label_names.get(lid, lid)} ({n})"
        table.add_row(
            str(i),
            domain,
            f"{count:,}",
            f"{share:.1f}%",
            str(senders),
            f"+{share:.1f}%",
            label_signal,
        )

    console.print(table)


def create_label(service, name: str) -> dict:
    body = {
        "name": name,
        "labelListVisibility": "labelShow",
        "messageListVisibility": "show",
    }
    return execute_with_backoff(
        service.users().labels().create(userId="me", body=body),
        f"Creating label {name}",
    )


def choose_labels(service, labels: list[dict], suggested_counts: Counter) -> list[dict] | None:
    user_labels = [l for l in labels if l.get("type") == "user"]
    by_id = {l["id"]: l for l in user_labels}
    by_name = {l["name"].lower(): l for l in user_labels}

    ranked = []
    for lid, count in suggested_counts.most_common(5):
        if lid in by_id:
            ranked.append((by_id[lid], count))

    if not ranked:
        for label in sorted(user_labels, key=lambda x: x["name"].lower())[:12]:
            ranked.append((label, 0))

    console.print("\n[bold]Where should it go?[/bold]")
    if suggested_counts:
        console.print("[dim]Existing labels already seen on messages from this domain are ranked first.[/dim]")

    for i, (label, count) in enumerate(ranked, 1):
        suffix = f"  [dim]({count} messages already use it)[/dim]" if count else ""
        console.print(f"  [cyan]{i}[/cyan]  {label['name']}{suffix}")

    console.print("  [cyan]t[/cyan]  Type label name(s), comma-separated")
    console.print("  [cyan]0[/cyan]  Cancel")

    choice = Prompt.ask("Label", default="1" if ranked else "t").strip()

    if choice == "0":
        return None

    if choice.lower() == "t":
        raw = Prompt.ask("Label name(s), comma-separated").strip()
        names = [x.strip() for x in raw.split(",") if x.strip()]
        if not names:
            console.print("[red]No labels entered.[/red]")
            return None

        selected = []
        for name in names:
            existing = by_name.get(name.lower())
            if existing:
                selected.append(existing)
                continue

            if Confirm.ask(f"Create new Gmail label [bold]{name}[/bold]?", default=True):
                created = create_label(service, name)
                labels.append(created)
                by_name[name.lower()] = created
                selected.append(created)

        return selected or None

    if choice.isdigit():
        index = int(choice)
        if 1 <= index <= len(ranked):
            return [ranked[index - 1][0]]

    console.print("[red]Invalid choice.[/red]")
    return None

def create_filter(service, domain: str, sender: str | None, label_ids: list[str], whole_domain: bool, skip_inbox: bool):
    # Domain matching uses Gmail's supported advanced-search syntax in criteria.query.
    if whole_domain:
        criteria = {"query": f"from:(@{domain})"}
        human_match = f"@{domain}"
    else:
        criteria = {"from": sender}
        human_match = sender

    action = {"addLabelIds": label_ids}
    if skip_inbox:
        action["removeLabelIds"] = ["INBOX"]

    body = {"criteria": criteria, "action": action}
    result = execute_with_backoff(
        service.users().settings().filters().create(userId="me", body=body),
        "Creating Gmail filter",
    )
    return result, human_match


def review_top(service, cov: Coverage, labels: list[dict]) -> None:
    remaining_domains = Counter(cov.uncovered_by_domain)
    current_pct = cov.pct

    while remaining_domains:
        domain, count = remaining_domains.most_common(1)[0]
        total = cov.total or 1
        gain = count / total * 100
        senders = cov.domain_senders.get(domain, Counter())
        top_sender = senders.most_common(1)[0][0] if senders else None

        sender_lines = "\n".join(
            f"  {sender:<44} {n:>5}"
            for sender, n in senders.most_common(8)
        )
        console.print(
            Panel(
                f"[bold]{domain}[/bold]\n"
                f"{count:,} uncovered messages · {len(senders)} senders\n"
                f"Fixing the whole domain could move coverage [green]+{gain:.1f}%[/green]\n\n"
                f"[dim]{sender_lines}[/dim]",
                title="🎯 Next best action",
                border_style="magenta",
            )
        )

        if not Confirm.ask("Review this opportunity now?", default=True):
            return

        whole_domain = Confirm.ask(
            f"Match the whole domain [bold]@{domain}[/bold]? "
            f"(No = only {top_sender})",
            default=len(senders) > 1,
        )
        sender = None if whole_domain else top_sender

        selected_labels = choose_labels(
            service, labels, cov.domain_labels.get(domain, Counter())
        )
        if not selected_labels:
            return

        label_names = ", ".join(label["name"] for label in selected_labels)

        skip_inbox = Confirm.ask(
            f"Skip Inbox for matching mail and apply [bold]{label_names}[/bold]?",
            default=True,
        )

        console.print(
            Panel(
                f"Match: [bold]{'whole domain' if whole_domain else 'sender'}[/bold]\n"
                f"From: [cyan]{'@' + domain if whole_domain else sender}[/cyan]\n"
                f"Apply label(s): [cyan]{label_names}[/cyan]\n"
                f"Skip Inbox: [cyan]{'yes' if skip_inbox else 'no'}[/cyan]",
                title="Rule preview",
                border_style="yellow",
            )
        )

        if not Confirm.ask("Create this Gmail filter?", default=False):
            console.print("[dim]No changes made.[/dim]")
            del remaining_domains[domain]
            if not remaining_domains or not Confirm.ask("Try the next best opportunity?", default=True):
                return
            continue

        result, human_match = create_filter(
            service,
            domain,
            sender,
            [label["id"] for label in selected_labels],
            whole_domain,
            skip_inbox,
        )

        realised_gain = gain if whole_domain else (
            cov.uncovered_by_sender.get(sender, 0) / total * 100 if sender else 0
        )
        new_pct = min(100.0, current_pct + realised_gain)

        console.print(
            Panel(
                f"[green bold]✓ FILTER CREATED[/green bold]\n\n"
                f"{human_match} → {label_names}\n\n"
                f"{current_pct:.1f}%  {bar(current_pct, 28)}\n"
                f"{new_pct:.1f}%  {bar(new_pct, 28)}\n\n"
                f"[bold green]+{realised_gain:.1f}% potential future coverage[/bold green]\n"
                f"[dim]Filter ID: {result.get('id')}[/dim]",
                border_style="green",
            )
        )

        current_pct = new_pct

        if whole_domain:
            del remaining_domains[domain]
        else:
            remaining_domains[domain] -= cov.uncovered_by_sender.get(sender, 0)
            if remaining_domains[domain] <= 0:
                del remaining_domains[domain]

        if not remaining_domains:
            console.print(Panel("[bold green]No uncovered traffic remains in this scan. 🎉[/bold green]", border_style="green"))
            return

        if not Confirm.ask("Create another rule from this scan?", default=True):
            return

    console.print(Panel("[bold green]Nothing else to fix from this scan. 🎉[/bold green]", border_style="green"))

def run(period: str, interactive: bool = True) -> None:
    banner()
    creds = get_credentials()
    service = build("gmail", "v1", credentials=creds, cache_discovery=False)

    profile = execute_with_backoff(service.users().getProfile(userId="me"), "Reading Gmail profile")
    console.print(f"[dim]Account: {profile.get('emailAddress', 'me')}[/dim]")

    start, end, period_label = period_bounds(period)
    query = f"after:{gmail_date(start)} before:{gmail_date(end)} -in:sent"

    labels = execute_with_backoff(
        service.users().labels().list(userId="me"), "Reading Gmail labels"
    ).get("labels", [])
    label_names = {l["id"]: l["name"] for l in labels}
    user_label_ids = {l["id"] for l in labels if l.get("type") == "user"}
    filters = execute_with_backoff(
        service.users().settings().filters().list(userId="me"), "Reading Gmail filters"
    ).get("filter", [])

    with console.status("[bold cyan]Finding messages…[/bold cyan]"):
        ids = list_message_ids(service, query)
    console.print(f"[dim]Found {len(ids):,} messages for {period_label}.[/dim]")
    rows = fetch_messages(service, ids)

    cov = analyse(rows, filters, user_label_ids)
    show_summary(cov, period_label, label_names)

    if interactive:
        review_top(service, cov, labels)


def auth_only() -> None:
    banner()
    get_credentials()
    console.print(Panel("[green]Authentication is ready.[/green]", border_style="green"))


def logout() -> None:
    if TOKEN_FILE.exists():
        TOKEN_FILE.unlink()
        console.print(f"[green]✓ Removed saved token:[/green] {TOKEN_FILE}")
    else:
        console.print("[dim]No saved token found.[/dim]")


def make_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="gmail-coverage",
        description="Measure Gmail routing-rule coverage and fix the most impactful gap.",
    )
    sub = p.add_subparsers(dest="command")

    test = sub.add_parser("test", help="Run the coverage test")
    test.add_argument(
        "--period",
        choices=["today", "week", "month", "quarter", "last-quarter", "year"],
        default="month",
    )
    test.add_argument("--no-fix", action="store_true", help="Report only; do not offer to create a rule")

    sub.add_parser("auth", help="Set up or refresh Gmail authorisation")
    sub.add_parser("logout", help="Delete the locally cached OAuth token")

    return p


def main() -> None:
    parser = make_parser()
    args = parser.parse_args()

    if not args.command:
        # Friendly default: run the useful thing rather than just showing argparse help.
        args.command = "test"
        args.period = "month"
        args.no_fix = False

    try:
        if args.command == "auth":
            auth_only()
        elif args.command == "logout":
            logout()
        elif args.command == "test":
            run(args.period, interactive=not args.no_fix)
    except KeyboardInterrupt:
        console.print("\n[yellow]Cancelled. No drama.[/yellow]")
        raise SystemExit(130)
    except HttpError as e:
        if is_quota_error(e):
            console.print(
                Panel(
                    "[red bold]Gmail is still rate-limiting this account after several retries.[/red bold]\n\n"
                    "Your authentication is fine and cached scan progress has been kept. "
                    "Running the command again will reuse cached message headers and continue with far fewer API reads.",
                    title="Quota limit reached",
                    border_style="red",
                )
            )
        else:
            console.print(Panel(f"[red bold]Gmail API error[/red bold]\n\n{e}", border_style="red"))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
