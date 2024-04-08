# Bake It Up

## Introduction

Bake It Up is a concept of a bakery based in Dublin where customers have the option to place orders for bread, pastries and cakes, with the ability to alter the properties of their goods to their liking. The aim of the website is to provide an online platform that allows its user's access to the same range of possibilities as they would be given if they were to place their order in-store, along with fully automating the commercial process, from accepting payments to compiling a list of orders for the day.

This e-commerce website was produced using Stripe Payments and the Django framework, and was designed with the help of Bootstrap.

![The home page of the Bake It Up website, displayed on a desktop screen](media/images/readme/bake-it-up.JPG)

## Design Thinking Process

> *"Why would a user want to visit our website?"*

- To make an order of bread, pastries and/or cakes online
- To get more information about the bakery

> *"What would make them return?"*

- A user-friendly website that makes the ordering process as simple and pain-free as possible
- An assortment of controls and options to change their orders where they see fit

### Problem Statement

*"How can we fully transfer the creative freedoms that our in-person patrons have into the online world?"*

### Solutions

> *"Why would a user want to visit our website?"*

- To make an order of bread, pastries and/or cakes online
  - Bake It Up's products are easily accessible throughout the site, with each category of products situated within the navigation at the top of the page
  - Products can be filtered by category, searched using a query, and sorted by their name, price, and number of favourites, in ascending or descending order. This makes finding products much easier as users can simply input their most desired features they are looking for in their products
  - Logged in users can also add products to their favourites, as well as filter products to only display their favourites, which is extremely useful for regular customers regularly buying their usual items, as they don't need to navigate through the products they know they don't want
- To get more information about the bakery
  - Upon entering the site, users are greeted with an array of images in the form of a carousel, in order to display a high volume of information distributed in an easy-to-read manner, while also taking up minimal space
  ![The home page, comprised of a carousel and general info about the bakery](media/images/readme/design-thinking/home-page.JPG)
  - Each image in the carousel is accompanied with a short sentence and a CTA button, allowing the users to directly maneuver to the part of the site that peaks their interest
  - The details about the physical bakery are present in the footer of every page. This is a general standard for most business websites. Here, users can find information about the address of the business, their phone number, email address and opening hours.

> *"What would make them return?"*

- A user-friendly website that makes the ordering process as simple and pain-free as possible
  - As described above, adding products to the user's cart is designed to be as straightforward as possible
  - Once the user is happy with their order, the process of checking out is also simple, hiding the delivery section behind a checkbox to prevent an overwhelming clutter of inputs for users not looking to have their products delivered
  - Logged in users can save their information to their profile, making their next order even easier as they no longer have to fill out their details again
- An assortment of controls and options to change their orders where they see fit
  - Every product can have multiple properties attached to it. These properties for each category are as follows:
    - **Bread**: shape, size and contents
    - **Pastries**: type, contents, colour, icing, decoration and text
  - Pastry products have more options because they are more complex than breads, and can be made of multiple parts and can have differnt layers
  - These properties have been implemented to only be a guideline, and can be freely edited to say whatever is applicable to the product

## Features

### Home Page

- The home page is the first thing that users see upon entering the site. It gives a short description about the company, what it does and its origins. This gives the users a brief insight into the personality of the bakery, allowing the bakery to display their interest in their craft, further highlighting the quality of their products
![]()
- Users who continue to read into the history are then brought to a short list of their most popular products

### Product Lists

#### Categories

#### Search for a Product

#### Sort Products

### View Products

#### Add to Favourites

### Shopping Cart

### Checkout

### Account Settings

### Store Contact

## Admin Features

### View Daily Orders

### View Messages

### Add/Edit Products

## Design

### User Interface

### Content Layout

### Color Scheme

### Typography

### Wireframes

## Business Model

## Search Engine Optimization

### Keywords

### "sitemap.xml" and "robots.txt" Files

## Web Marketing

<details><summary><strong>Newsletter</strong></summary>

- Instead of relying on an external program to deliver newsletters, admins can send newsletters within the website itself, accessed through the profile dropdown on any page. This was done as there is extra functionality to Bake It Up's newsletter, which includes automatically applying discount codes to its subscribers.
- The user can enter:
  - A subject, which will appear first in the subscriber's inbox
  - A message body, which is where the bulk of the content will be entered
  - A discount code, which will give subscribers a sum of money off of their next order
- A base is provided to give a structure to the newsletter. This includes:
  - A header, indicating that the email is a Bake It Up newsletter, which is accompanied by the date it was sent.
  - A format for the discount code, if applicable
  - A signature
  - A link to unsubscribe to the newsletter

![The "Send Newsletter" form](media/images/readme/web-marketing/newsletter/newsletter-form.JPG)

- The newsletter includes a preview that shows how the newsletter will look in the email. This is to prevent any mix-ups between the admin's input and the base format, for example, the admin entering a signature at the bottom of the message when a signature already exists in the template
- This preview updates when the admin changes their message, without the need of any annoying "Generate Preview" buttons 

![A newsletter preview](media/images/readme/web-marketing/newsletter/newsletter-preview.JPG)

- A discount code can be added to the newsletter by checking the checkbox to add the discount code. The code inputs are disabled when this box is unchecked to prevent confusion in admins thinking these inputs always have to be filled out.

![The discount code section](media/images/readme/web-marketing/newsletter/discount-code.JPG)

- Discount codes include a code name, which is what is used to access the code in the checkout page
- Code names must be unique, and cannot contain spaces or special characters other than "-"
- Code names are checked for errors when the user updates them, allowing the user to immediately correct any errors

![An error displayed for an invalid code name](media/images/readme/web-marketing/newsletter/discount-error.JPG)

- Invalid code names are displayed in the preview, ensuring the admin will be made aware of the error

![An error displayed in the preview](media/images/readme/web-marketing/newsletter/discount-preview-error.JPG)

- If the structure of the code name is valid, with the use of *Asynchronous JavaScript and XML* (AJAX), the server is checked in real time to see if the name is already present in the database. This allows the user to, again, immediately correct this error, without having to submit the form first

![A name already in use](media/images/readme/web-marketing/newsletter/existing-code.JPG)

- Discount codes have another property, the discount value, which is the amount the discount will take off the cart total
- The property is comprised of several components:
  - The discount value, which is how much the discount applied will be
  - The discount type, which can take the form of a fixed amount of money or a percentage taken off the order, relative to the discount value
  - An optional minimum spending amount, which the cart total needs to surpass in order for the discount code to take effect
- This complex structure was made quite simple to understand using an inline form made to resemble a sentence describing the deal.

![The discount value](media/images/readme/web-marketing/newsletter/discount-value.JPG)

- Once a valid discount code has been created, the format that will be displayed in the newsletter appears in the preview

![A valid discount code displayed in the preview](media/images/readme/web-marketing/newsletter/discount-preview.JPG)

- Once a newsletter is sent, the user receives the email, and has the discount code applied to their email address, which can be viewed in the user profile page

![A newsletter in my email](media/images/readme/web-marketing/newsletter/newsletter-received.JPG)

![The discount code applied](media/images/readme/web-marketing/newsletter/discount-applied.JPG)

</details>

### Facebook Page

### Instagram Page

## Agile Methodologies

Bake It Up was developed using an Agile methodology

- All areas of the site were planned out in the beginning of the development, in the form of *user stories*, which are abilities that users of the site are able to use

![A list of user stories to be completed throughout the development of Bake It Up](media/images/readme/agile-methodologies/user-stories.JPG)

- Contrary to a standard task found in waterfall development, a user story also explains the purpose of that task, and why it would be useful for a user of the site. It takes the form of:
  > *"As a **role**, I can **ability** so that **purpose**"*
  Where:
    - **Role**: The type of user engaging with the site. I mainly used "User" (meaning customer) and "Site Administrator" (meaning person(s) responsible for running the site)
    - **Ability**: The feature of the site the user story is referring to. For example: "View my shopping cart"
    - **Purpose**: The reason the feature should exist. If no valid reason can be found, then the time spent implementing this feature could be better spent elsewhere. For example: for my "View my shopping cart" ability the purpose would be that "I can see all the products I have ordered"

![The details of a user story](media/images/readme/agile-methodologies/user-story-details.JPG)

- User stories also have other properties, such as:
  - **Epics**: This is a form of grouping of similar user stories. For example: the user story "Log in to my account" would belong to the epic "Authentication". Epics were assigned to user stories through the use of *orange* coloured labels
  - **Themes**: This is a more broad type of user story grouping, which groups epics together. For example, the epic "Authentication" would belong to the theme "Accounts". Themes were assigned to user stories through the use of *cyan* coloured labels
  - **Story Points**: These are numbers assigned to user stories that give a rough estimation of how long it would take to complete that user story. There is no fixed time to measure these points, but instead, the best method would be to compare them to other user stories. Story points were assigned to user stories in the form of *green* coloured labels

![The properties of a user story](media/images/readme/agile-methodologies/user-story.JPG)

- The development cycle of the website was broken down into week-long timelines called *iterations*. Each iteration had a set list of user stories that were aimed to be completed by the end of that iteration
- Each user story assigned to the iteration was given one of three labels:
  - "Must Have": This user story is required to be completed during this iteration
  - "Should Have": This user story is not required, but it is recommended to complete this within the iteration
  - "Could Have": This user story is not required, but if all other user stories are completed, try to complete these
- "Must Have" user story points must not exceed 60% of the total amount of story points in an iteration
- Bake It Up took 6 iterations to complete all the user stories

<details><summary>View all iterations for Bake It Up</summary>

  ### Iteration 1
  ![Iteration 1](media/images/readme/agile-methodologies/iteration-1.JPG)
  
  ### Iteration 2
  ![Iteration 2](media/images/readme/agile-methodologies/iteration-2.JPG)

  ### Iteration 3
  ![Iteration 3](media/images/readme/agile-methodologies/iteration-3.JPG)

  ### Iteration 4
  ![Iteration 4](media/images/readme/agile-methodologies/iteration-4.JPG)

  ### Iteration 5
  ![Iteration 5](media/images/readme/agile-methodologies/iteration-5.JPG)

  ### Iteration 6
  ![Iteration 6](media/images/readme/agile-methodologies/iteration-6.JPG)

</details>

- Some user stories had an extra label, "NINTH" (short for Not Important, Nice To Have), which was reserved for extra features that were not fundamental to the website

![A user story with the label "NINTH"](media/images/readme/agile-methodologies/ninth.jpg)

- Throughout the development process, some of these "NINTH" user stories were decided to be removed outright from the final project. Instead of deleting these, I decided to label these user stories with the label "Won't Have", meaning they would not be implemented into the final product

![The "Won't Have" user stories left at the end of the project](media/images/readme/agile-methodologies/wont-haves.JPG)

## Data Models

![A list of all models used for Bake It Up](media/images/readme/data-models/model-list.JPG)

### CRUD Functionality

## Testing

### Manual Testing

### Automated Testing

### Browser Testing

### Error Handling

#### 404 Page

- If a page that has been requested by the user is not found, they are instead redirected to a 404 page, where they are notified that what they are looking for doesn't exist, or has existed before but has been deleted
- Users are then given a link to return to the home page, so they are not left stuck at an error page and are directed back to the site flow

![The body of the 404 page](media/images/readme/testing/error-handling/404-page.JPG)

#### 500 Page

- 500 errors will result in the user taken to a 500 error page, which takes a similar form to the 404 page
- However, any errors found in the program will be sent to the admins through the store contact messaging system. This allows for a quick response to any errors found within the site, as the admins can contact the active developer and report the issue
- To test this, I will type the code snippet `hello.world()` into the home page view. "hello" is not defined anywhere in the program, resulting in an error

![hello.world error code](media/images/readme/testing/error-handling/500-error-code.JPG)

![Viewing the home page after inserting the faulty code](media/images/readme/testing/error-handling/500-error-test.JPG)

- The error successfully results in the user being redirected to the 500 page, with a brief paragraph explaining that the staff have been notified of the issue
- The paragraph ends with a link to return to the home page, in a similar fashion to the 404 page
- No details are given about the error in the 500 page. This is done to prevent any private information, such as environment variables in use in the code, becoming exposed the public, as well as preventing the confusion of users who would have no idea how to interpret the error

![A message has appeared for the admin](media/images/readme/testing/error-handling/500-message-received.JPG)

- Meanwhile, on an admin account, a message notification has appeared in the top right of the profile dropdown. This message is about the error we just experienced.
- Once the admin views the message, the error gives a basic description of the error, giving the receiver the view where it happened and the error message
- At this point, the site owner can contact the developer and the issue can be solved with haste

![The error message](media/images/readme/testing/error-handling/error-message.JPG)

## Validation

### W3C HTML

### W3C CSS

### JSHint

### PEP8

### Lighthouse

## Deployment and Local Development

### Deployment to Heroku

### Cloning Repositories

### Forking Repositories

## Other points to note

### Naming conventions

## Credits

### Code Snippets/Tutorials

### Media