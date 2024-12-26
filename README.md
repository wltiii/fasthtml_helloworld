# FastAPI with HTMX

## Introduction

This project presents a simple example of using FastHTML. Nothing fancy. I expect to expand upon this with more complex examples in the future.

## Notes on Design

### Single-page vs. Multi-page Approach

It is not inherently wrong to use a multi-page approach. It's worth considering the trade-offs and alternatives.

Single-page web apps (SPAs): a SPA is a web application that loads a single HTML page and dynamically updates the content as the user interacts with the app. SPAs typically use JavaScript frameworks like React, Angular, or Vue.js to manage the application state and render the UI. FastHTML is the new kid on the block in this game. I like this for its integration with Python, FastAPI, and HTMX.

In contrast, a design using multiple Python files, each serving a separate HTML page can work, it might lead to some limitations and drawbacks:

- More complex routing: With multiple applications, you'll need to manage routing between them, which can become complex.
- Increased overhead: Each application will have its own overhead, such as separate FastAPI instances, templates, and static files.
- Less cohesive user experience: Since each application is separate, you might need to duplicate functionality or share data between them, which can lead to inconsistencies.

That being said, there are scenarios where a multi-page app approach makes sense:

- Simple, independent applications: If each application is relatively simple and independent, with minimal shared functionality, a separate Python file for each might be a good choice.
- Legacy system integration: If you're integrating with existing systems or applications, a multi-page app approach might be necessary to accommodate the existing architecture.

### Inlining HTML vs. Separating HTML

In-line HTML is a perfectly valid approach, especially when working with small to medium-sized applications. In fact, FastAPI's built-in support for returning HTML strings makes it easy to do so.

There are no technical reasons why you can't or shouldn't in-line your HTML. However, here are some considerations to keep in mind:

- Readability and maintainability: As your application grows, in-lined HTML can make your Python code harder to read and maintain. You might find yourself scrolling through a long string of HTML, trying to find a specific element or fix a bug.
- Separation of concerns: In-lined HTML blurs the line between your application's logic and presentation. While it's not a hard and fast rule, separating concerns can make your code more modular and easier to work with.
- Reusability: If you need to reuse a piece of HTML in multiple places, in-lined HTML can make it harder to do so. You might end up duplicating code or creating a separate function to render the HTML.

That being said, if you're comfortable with in-lined HTML and your application is relatively small, it's not a problem. FastAPI is designed to be flexible, and you can use it to return HTML strings in whatever way works best for your project.

## Conclusion

*Remember, it's okay to take things one step at a time and iterate on your design.* You can always refactor or improve your code later.

Good luck with your project!
