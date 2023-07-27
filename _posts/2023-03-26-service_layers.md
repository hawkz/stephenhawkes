---
layout:     post
title:      Learning Service Layers
date:       2023-03-26 20:00
summary:    What's next for service layers?
categories: blog
---

## The Importance of Service Layer Reuse for Charities and Non-Profit organisations
As charities and non-profit organisations increasingly rely on digital platforms to deliver services and engage with supporters, it becomes crucial to develop efficient and effective systems that can handle large amounts of data and user interactions. Service layer reuse, or the practice of developing modular and reusable components that can be shared across different projects, can significantly improve the efficiency and effectiveness of digital projects while reducing development costs and complexity.

### Why Service Layer Reuse Matters
Service layer reuse has already proven its value in many sectors, such as finance and e-commerce. By building reusable components that encapsulate common functionality and business logic, developers can focus on delivering unique features and user experiences instead of re-implementing the same basic functionality for every project. This approach can also help ensure consistency and reliability across different projects, reduce the risk of errors, and speed up development time.

For charities and non-profit organisations, service layer reuse can have even greater benefits. By implementing reusable search functionality and notification services, for example, charities can enhance their ability to find and engage with supporters, while also enabling more efficient and effective management of data and resources. These services can be integrated into various projects and platforms, from fundraising campaigns to volunteer management systems, allowing charities to work more efficiently and effectively.

![OODA Loop](/img/ooda.svg)

## Starting with 4 service layers
- **Search**: Search functionality can be a valuable service layer for the third sector, particularly for organisations that have large amounts of data or resources. By creating a search service that can be integrated into different applications or websites, organisations can make it easier for users to find the information they need.
- **Notifications**: Notifications can help keep users engaged and informed about important updates or events. A reusable notification service can be used across multiple applications or websites to ensure that users receive timely and relevant information. This case started with the reuse of the GDS notifications framework.
- **Blockchain case referrals**: Blockchain technology can be used to create secure and transparent case management systems for the third sector. By creating a blockchain-based service layer, organisations can improve accountability, reduce the risk of fraud, and streamline case management processes.
- **Resource hubs**: Resource hubs can be a valuable service for the third sector, particularly for organisations that provide support services to vulnerable populations. By creating a reusable resource hub service, organisations can make it easier for users to access information about available resources, such as food banks, shelters, and mental health services.

### The learning from the process so far
From the work done so far we’ve learned that the project that involved end-users in the development of a resource hub had a higher chance of being successful and reusable in the future because the need for the resource hub was established through the involvement of the end-users. By involving end-users, the project was able to understand their needs and preferences, and tailor the resource hub to meet those needs. Additionally, Resource Hubs had a sustainable source of income and a ready-made audience when it was completed. This means there was a clear  plan for how it would be funded and sustained over time, and there was already a group of people who were interested in using the resource hub. That was hard to predict during the build process, but looking back was a key component in the project’s success.

The learning from this is that when developing service layers and reusable components, it's important to start with a clear understanding of the needs of the end-users. By involving end-users in the development process, the project can ensure that the service layer or reusable component meets their needs and is therefore more likely to be successful and reusable in the future. Furthermore, having a sustainable source of income and a ready-made audience can help ensure the longevity of the project and increase the likelihood that it will be reused in the future. It's important to consider these factors when developing service layers and reusable components, as they can greatly impact the success and sustainability of the project.

## Identifying Overlap of Needs and Opportunities
One useful technique for identifying overlap of needs and opportunities for service layer reuse is to use functional stories. Functional stories are short descriptions of user needs that focus on what the user wants to accomplish, rather than how the system will achieve it. By developing a library of functional stories, charities can identify common patterns and needs across different projects and platforms, and develop reusable services that address those needs.

For example, a functional story might describe the need for a notification service that sends automatic reminders to volunteers about upcoming events. By analysing similar stories across different projects, charities can identify opportunities to develop a reusable notification service that can be integrated into multiple systems, reducing the need for custom development and testing.

## Functional stories as a mechanism
Creating service layers and reusable components is a powerful way to improve the impact and longevity of digital tools and services. But to create solutions that are widely used and reusable, we need to start with a deep understanding of user needs and the priorities of different organisations. This approach can help us identify areas of overlap in needs and create solutions that are more likely to be successful and reusable.

However, one challenge we've encountered is a lack of common language between projects. User stories are great for capturing user needs, but they don't always provide a clear way to define the functionality of a digital tool or service. This is where functional stories come in.

Functional stories describe what a piece of software does, rather than focusing on the user's needs. A useful way to structure functional stories is to follow the format:
> "[**context/tool**] takes [**input data**] and does [**process**] to [**output or effect**]".

This concise structure can help to define the utility of a digital tool or service and identify areas of overlap in needs across different organisations.

For example, a functional story for a search component might be:
> "The search tool takes a keyword query and searches a database of articles to return a list of relevant articles." 

This functional story clearly defines the function of the search tool, allowing for a better understanding of its utility and potential for reuse.

By using functional stories, we can create a shared language between projects and better understand the functionality of digital tools and services. This can help us identify areas of overlap in needs and create reusable service layers or components that can be used by multiple organisations to address similar needs.

Overall, creating a common language between projects is a crucial step in the process of creating reusable service layers and components. Functional stories provide a clear and concise way to define the functionality of digital tools and services, which can help us identify areas of overlap in needs and create solutions that are more likely to be successful and reusable.

Every system can be distilled down to inputs, processes and outputs, and the common overlaps can be more easily understood using this format. It also abstracts away the 

| Tool / Context               | Input                              | Process                                      | Output                                         |
| ---------------------------- | ---------------------------------- | -------------------------------------------- | ---------------------------------------------- |
| Organisation website         | Text, Images, Videos, Links        | Render web pages with content and navigation | A functioning website                          |
| Online collaboration tools   | Text, Documents, Presentations     | Allow multiple users to edit and share files | Collaboratively created and stored documents   |
| Database / CRM               | Customer Data                      | Store and manage customer information        | Organised and easily accessible customer data  |
| Internal communication tools | Messages, Files, Meetings          | Facilitate real-time communication           | Improved internal communication and efficiency |
| Financial accounting         | Transactions, Invoices, Receipts   | Record and track financial transactions      | Accurate financial records and reporting       |
| Project management tools     | Tasks, Deadlines, Milestones       | Plan and manage project tasks and progress   | Organised and efficient project management     |
| Fundraising database         | Donor Data                         | Store and manage donor information           | Organised and easily accessible donor data     |
| Social media                 | Posts, Comments, Followers         | Share and interact with content              | Increased online engagement and reach          |
| Data collection tools        | Survey Questions, Response Data    | Collect and analyse data                     | Organised and meaningful data insights         |
| HR software                  | Employee Data, Payroll Information | Store and manage employee information        | Organised and easily accessible HR data        |

The keen observers amongst you will spot that this has actually resulted in something very similar to the CIPO model used in schooling. This could be a great pattern for the incorporating the context of the charity or group into the table. Allowing searching for common contexts, common inputs, common processes and common outputs.

## Addressing Challenges
While service layer reuse offers many benefits, there are also challenges that charities and non-profit organisations may face when implementing this approach. For example, building reusable services requires careful planning and design, as well as expertise in software architecture and development. To address these challenges, organisations such as CAST, Catalyst, and The Developer Society provide resources and support to help charities build capacity and improve their digital skills.

Another potential solution is to shape tools as software-as-a-service (SaaS) services that can be easily integrated into existing systems. This approach can help reduce the need for custom development and maintenance, while also providing access to a wider range of features and functionality.

### Becoming a research project...
The statement you're referring to suggests that the initiative has shifted its focus from creating new service layers to better understanding existing needs and finding ways to connect those needs with software that can be reused.

This approach acknowledges that the goal of service layers and reusable components is to address specific needs or problems, rather than simply creating more layers or components for their own sake. By starting with a deep understanding of the needs that exist, the initiative can identify areas where software could be developed or repurposed to meet those needs.

This approach can be more effective because it starts with the end-users and their needs, rather than starting with a technology solution and trying to find a problem to solve. By focusing on the needs that exist, the initiative can identify opportunities for software reuse that are more likely to be successful and impactful.

Overall, this approach prioritizes a user-centered design approach and can lead to more effective and sustainable solutions. Rather than creating more layers or components that may not be useful or effective, the initiative can focus on creating solutions that meet specific needs and can be reused over time.

## Funder analysis to reuse
Starting with funders as the source of enabling use can be an effective way to explore the potential for service layer reuse. By understanding the funding priorities of different organisations, it's possible to identify areas where there is overlap in the needs that they are trying to address. This overlap can then be used as a starting point for developing service layers or reusable components that can be used by multiple organisations.

One way to identify this overlap is to look at past funding data. By analysing the types of projects that have been funded in the past, it's possible to identify areas where there is significant overlap in the needs that organisations are trying to address. For example, if multiple organisations have funded projects related to food security or homelessness, it may be possible to develop a reusable service layer or component that addresses those needs more broadly.

The resource hub project is a good example of this approach in action. By starting with a deep understanding of the needs of end-users and the funding priorities of different organisations, the project was able to identify a need for a resource hub that could be used by multiple organisations to provide information and support to vulnerable populations. This need was established through engagement with funders and end-users, which helped to ensure that the resource hub was developed with a clear understanding of the needs that it was intended to address.

Overall, starting with funders as the source of enabling use can be an effective way to explore the potential for service layer reuse. By understanding the funding priorities of different organisations and identifying areas of overlap in their needs, it's possible to develop reusable service layers or components that can be used to address those needs more broadly. This approach can help to ensure that service layers and components are developed with a clear understanding of the needs they are intended to address, which can increase their impact and sustainability over time.

## Conclusion
Service layer reuse offers significant benefits for charities and non-profit organisations, enabling them to build more efficient and effective digital systems while reducing development costs and complexity. By identifying common patterns and needs across different projects and platforms, organisations can develop reusable services that enhance their ability to engage with supporters, manage data, and deliver services. While implementing service layer reuse requires careful planning and design, organisations can leverage the resources and support of various initiatives to build capacity and improve their digital skills.
