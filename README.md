<p align="center"> #Art by Cecilia </p>

---

<div align="center">

##  **Project Overview**

</div>

> **Our team of four navigated the challenge of integrating multiple Django apps**—collections, events, owner management, and store functionality—while maintaining a cohesive user experience across visitor-facing galleries and administrative dashboards. 
> 
> ### **The Biggest Win**
> 
> Successfully implementing a **full-stack e-commerce platform** featuring:
> -  **Cloudinary image optimization**
> -  **Dynamic theming** with 20+ Google Font combinations
> -  **Sophisticated messaging system** connecting visitors directly with the artist
> 
> ###  **Delivered Through Collaborative Agile Sprints**
> 
> Tracked on our Kanban board, we delivered:
> - ✅ CRUD operations for artworks and exhibitions
> - ✅ Integrated Stripe payments for testing
> - ✅ Production-ready Heroku deployment with PostgreSQL
> - ✅ Responsive design and accessibility standards across all devices
>
> <br>
>
> **Prepared by:** [Dylan](https://github.com/DylanAustin-TheDreamer) • [Ryan](https://github.com/zZWinterZz) • [Valentyna](https://github.com/Val916) • [Rebekah](https://github.com/Rebekah-codes)

---

Art that remembers. Const Collection by Cecilia K. is a quiet revolution—paintings that reclaim the feminine, resist distortion, and invite you to collect what feels true.

This platform is designed to honor the artist's voice, showcase their evolving body of work, and invite visitors into a space of emotional resonance and thoughtful exploration. It blends storytelling, visual clarity, and intuitive navigation to serve artists, visitors, and buyers alike.

<br>

<p align="center">

Art that remembers. Const Collection by Cecilia K. is a quiet revolution—paintings that reclaim the feminine, resist distortion, and invite you to collect what feels true.

This platform is designed to honor the artist's voice, showcase their evolving body of work, and invite visitors into a space of emotional resonance and thoughtful exploration. It blends storytelling, visual clarity, and intuitive navigation to serve artists, visitors, and buyers alike.

<br>

<p align="center">
    <a href="https://constcollection.com/" target="_blank" rel="noopener noreferrer">
        <img src="https://github.com/DylanAustin-TheDreamer/const-collection-full-stack-hackathon/blob/main/collections_app/static/collections_app/images/readme-images/Cecilia.png" alt="Art by Cecilia" style="max-width:100%;height:auto;">
    </a>
    <br>
    <em>Artwork: Art by Cecilia K. — <a href="https://constcollection.com/" target="_blank" rel="noopener noreferrer">constcollection.com</a></em>
</p>

 **Deployed Link**: [Art by Cecilia](https://const-collection-0f06bd9d4705.herokuapp.com)

---

## Table of Contents

1. [Features](#features)
    - [Core Functionality](#core-functionality)
    - [User Experience](#user-experience)
    - [Administrative Features](#administrative-features)
    - [Wireframes](#wireframes)
    - [Color Scheme](#color-scheme)
    - [Typography](#typography)
    - [Imagery](#imagery)
2. [Technologies Used](#technologies-used)
    - [Backend](#backend)
    - [Frontend](#frontend)
    - [Cloud Services & Deployment](#cloud-services--deployment)
    - [Development Tools](#development-tools)
3. [E-Commerce & Payment System](#e-commerce--payment-system)
4. [User Stories & Planning](#user-stories--planning)
5. [Database Design](#database-design)
    - [ERD Diagram](#erd-diagram)
    - [Core Models](#core-models)
6. [Testing](#testing)
    - [Manual Testing Results](#manual-testing-results)
    - [Code Validation](#code-validation)
      - [HTML Validation](#html-validation)
      - [CSS Validation](#css-validation)
      - [Python Validation](#python-validation)
    - [Lighthouse Performance Testing](#lighthouse-performance-testing)
7. [Deployment](#deployment)
    - [Heroku Deployment Process](#heroku-deployment-process)
    - [Deployment Steps](#deployment-steps)
8. [AI Integration](#ai-integration)
9. [Credits and Acknowledgements](#credits-and-acknowledgements)
    - [Project Foundation](#project-foundation)
    - [Development Resources and Tools](#development-resources-and-tools)
    - [Content Sources and Media Attribution](#content-sources-and-media-attribution)
10. [Features Left to Implement](#features-left-to-implement)

---

## Features

### Core Functionality

- **Home Page**  responsive design [Here](https://github.com/DylanAustin-TheDreamer/const-collection-full-stack-hackathon/blob/main/staticfiles/collections_app/images/readme-images/About.png)
- **Store** - with possibility to search and sort [Here](https://github.com/DylanAustin-TheDreamer/const-collection-full-stack-hackathon/blob/main/staticfiles/collections_app/images/readme-images/Store.png) and [Here](https://github.com/DylanAustin-TheDreamer/const-collection-full-stack-hackathon/blob/main/staticfiles/collections_app/images/readme-images/Serch-by-name.png)
- **User Authentication** - Register, login, logout functionality [Here](https://github.com/DylanAustin-TheDreamer/const-collection-full-stack-hackathon/blob/main/staticfiles/collections_app/images/readme-images/SignOut.png)
- **Picture Management** - Create, read, update, and delete media, Art, Collections, About page or Exibitions for the Owner (CRUD) [Here](https://github.com/DylanAustin-TheDreamer/const-collection-full-stack-hackathon/blob/main/staticfiles/collections_app/images/readme-images/CRUDfortheOwner.png)
- **The About Page** is ![Here](https://github.com/DylanAustin-TheDreamer/const-collection-full-stack-hackathon/blob/main/staticfiles/collections_app/images/readme-images/About.png)
- **Payment** enable for testing for Admin [Here](https://github.com/DylanAustin-TheDreamer/const-collection-full-stack-hackathon/blob/main/staticfiles/collections_app/images/readme-images/Payment%20test%20for%20Admin.png)
-  **Sophisticated messaging system** — A three-tier communication platform enabling direct visitor-to-artist contact through public contact forms, real-time unread message tracking with badge notifications, and threaded conversation history where owners can reply directly through the platform with automatic email delivery to anonymous visitors

#### User Experience

- **Responsive Design** - Works perfectly on all devices [Here](https://github.com/DylanAustin-TheDreamer/const-collection-full-stack-hackathon/blob/main/staticfiles/collections_app/images/readme-images/Screenshot%202025-10-15%20111908.png)
- **Modern UI** - Clean, accessible interface with Bootstrap 5
- **Image Upload** - Cloudinary integration for images

#### Administrative Features

- **Admin Interface** - Full Django admin for content management [Here](https://github.com/DylanAustin-TheDreamer/const-collection-full-stack-hackathon/blob/main/staticfiles/collections_app/images/readme-images/Owner-Menu.png)

### Wireframes

## [Wireframes](http://bit.ly/43f0FE9)

### Color Scheme

Minimalist Palette Philosophy
This grayscale palette—ranging from pure white to absolute black—embodies the principles of minimalism: clarity, restraint, and emotional space. It serves as a neutral canvas that allows the artwork to speak without distraction, letting color-rich pieces radiate with full intensity.
Rainbowcolored hover Effects: Subtle hover effects on some buttons enhance user interaction, providing visual feedback when the button is hovered over, which encourages clicks.

<table>
    <thead>
        <tr>
            <th>Name</th>
            <th>Hex Code</th>
            <th>Usage </th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Pure White</td>
            <td>#FFFFFF</td>
            <td>Background, whitespace, clean canvas</td>
        </tr>
        <tr>
            <td>Light Gray</td>
            <td>#F5F5F5</td>
            <td>Section dividers, subtle hover effects</td>
        </tr>
        <tr>
            <td>Cool Gray</td>
            <td>#D3D3D3</td>
            <td>Card backgrounds, secondary text</td>
        </tr>
        <tr>
            <td>Medium Gray</td>
            <td>#A9A9A9</td>
            <td>Borders, muted buttons</td>
        </tr>
        <tr>
            <td>Charcoal Gray</td>
            <td>#555555</td>
            <td>Body text, icons</td>
        </tr>
        <tr>
            <td>Graphite</td>
            <td>#333333</td>
            <td>Headings, navigation bar</td>
        </tr>
        <tr>
            <td>Absolute Black</td>
            <td>#000000</td>
            <td>Accent text, high-contrast elements</td>
        </tr>
    </tbody>
</table>

---

[Color Palette](https://github.com/DylanAustin-TheDreamer/const-collection-full-stack-hackathon/blob/main/collections_app/static/collections_app/images/readme-images/palette-white-black.png)

### Typography

The site uses **Google Fonts**.
The project has a sophisticated **multi-theme system** where each theme (Scheme 1-20+) can use different font combinations. Here's how it works:

 All Available Google Fonts (loaded in base.html line 32):

2. Font Variables in Each Scheme (from CSS files):
Scheme 1 (Dark theme):

Headings: Playfair Display (serif)
Body: Montserrat (sans-serif)
Scheme 2 (Light museum theme):

Headings: Playfair Display (serif)
Body: Montserrat (sans-serif)
Scheme 3 (Taupe theme):

Headings: Playfair Display (serif)
Body: Montserrat (sans-serif)
3. How the Switch Happens (from schemes.css):

```css
/* CSS Variables control fonts */
:root {
    --font-heading: "Playfair Display", serif;
    --font-body: "Montserrat", sans-serif;
}

/* Applied globally */
body {
    font-family: var(--font-body, system-ui, ...);
}

h1, h2, h3, h4, h5, h6 {
    font-family: var(--font-heading, inherit);
}
```

When a user selects a different theme (Scheme 1, 2, 3, etc.), the corresponding Scheme-X.css file is loaded, which redefines --font-heading and --font-body, instantly changing all fonts across the site!

4. Where Users Change Themes:
The theme selector appears in the user dashboard with a radial selector showing theme dots that users can click to switch between schemes.

### Imagery

- **Source**: [Art by Cecilia K.](https://constcollection.com/)
- **Hosting**: [Cloudinary](https://cloudinary.com/) for optimized loading
- **Optimization**: Responsive images with proper aspect ratios

---

## Technologies Used

### Backend

### Backend

- **[Python 3.12](https://www.python.org/)** - Core language
- **[Django 4.2](https://www.djangoproject.com/)** - Web framework
- **[PostgreSQL](https://www.postgresql.org/)** - Database
- **[Django Allauth](https://django-allauth.readthedocs.io/)** - Authentication

### Frontend

- **[HTML5](https://developer.mozilla.org/en-US/docs/Web/HTML)** & **[CSS3](https://developer.mozilla.org/en-US/docs/Web/CSS)** - Markup & styling
- **[JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)** - Interactivity
- **[Bootstrap 5](https://getbootstrap.com/)** - UI framework
- **[Font Awesome](https://fontawesome.com/)** - Icons

### Cloud Services & Deployment

- **[Heroku](https://www.heroku.com/)** - Hosting
- **[Cloudinary](https://cloudinary.com/)** - Image optimization
- **[WhiteNoise](https://whitenoise.evans.io/)** - Static files

### Development Tools

- **[GitHub](https://github.com/)** & **[GitHub Copilot](https://github.com/features/copilot)** - Version control & AI assistance
- **[VS Code](https://code.visualstudio.com/)** - Code editor
- **[Chrome DevTools](https://developer.chrome.com/docs/devtools/)** - Debugging

---

## E-Commerce & Payment System

**Integrated Payment System**

A complete e-commerce checkout flow featuring:
- **Shopping basket functionality** with real-time item management, quantity updates, and persistent storage across sessions
- **Admin test checkout** enabling order creation with billing information capture (email, address, contact details)
- **Stripe integration prepared** with API configuration and payment processing architecture ready for production deployment
- **Order management system** that creates permanent order records with snapshot pricing, variant tracking, and automatic basket clearing upon successful checkout

Currently operational for admin testing with full Stripe payment processing infrastructure in place for future activation.

---

## User Stories & Planning

- **[Project Board](https://github.com/users/DylanAustin-TheDreamer/projects/15)**

The project was developed using Agile methodology [**(see Board in process)**](https://github.com/DylanAustin-TheDreamer/const-collection-full-stack-hackathon/blob/main/collections_app/static/collections_app/images/readme-images/project-board.png) with iterative progress and continuous feedback. User stories were tracked using a Kanban board to ensure systematic development, using categorized tasks into Must have, Should have, Could have, and Won’t have to clarify what’s essential, desirable, optional, or excluded for a project’s success. 
Here are some of the User Stories.

### As a visitor, I want to explore themed collections so I can engage with the artist’s evolving body of work.

**Acceptance Criteria:**

- Collections are displayed with titles, cover images, and brief descriptions.
- Clicking a collection opens a page with its artworks and artist statement.

**Tasks:**

1. Design collection model in Django (title, description, cover image).
2. Create gallery view for collections.
3. Link each collection to its artworks and statement.

</details>

<details>

  <summary>- As a visitor, I want to click on an artwork to see its full image, title, date, and description so I can appreciate it fully.
</summary>

**Acceptance Criteria:**

- Artwork thumbnails link to detail pages.
- Detail page includes full image, title, date, medium, dimensions, and description.

**Tasks:**

1. Create artwork detail template.
2. Add fields to artwork model.
3. Implement routing from gallery to detail view.

</details>

<details>

  <summary>- As a visitor, I want to filter artworks by medium (e.g., acrylic, mixed media) or style so I can find pieces that match my interests.</summary>

**Acceptance Criteria:**

- Filter options are visible and functional.
- Selecting a filter updates the gallery view dynamically.

Tasks:

1. Add medium/style fields to artwork model.
2. Implement filter logic in views.
3. Style filter UI with dropdowns or checkboxes.

</details>

<details>

  <summary>- As a visitor, I want to read the artist’s reflections for each collection so I understand the emotional and philosophical context.</summary>

**Acceptance Criteria:**

- Each collection includes a visible artist statement.
- Statement is readable and styled for clarity.

Tasks:

1. Add statement field to collection model.
2. Display statement on collection page.
3. Style typography for emotional impact.

</details>

<details>

  <summary>- As an artist, I want to group my work into series or themes so my portfolio feels cohesive and intentional.</summary>

**Acceptance Criteria:**
- Artist can assign artworks to a series.
- Series are displayed as part of the collection or separately.

Tasks:

1. Create series model and link to artworks.
2. Add series management to admin panel.
3. Display series grouping in gallery view.

</details>


## Database Design

### ERD Diagram

The Entity Relationship Diagram visually represents the structure of the database and the relationships between entities.


  - Click to view relationships between entities diagram 
  [Entities](https://mermaid.live/edit#pako:eNqtVdty2jAQ_RWPnoFpuDTgt5SkUyZpaCmZXoYZj7AUsxNbciU5CQH_e9cXgm2Ztg_xk609OnvOalfeEV8yTlzC1SXQQNFoJRx87r5dLZz9vtuVO-disfw-X1w7ruMrTg3XNmQ6v7m5mi5n81tEySfRArn68Wn2YVZCNlKbFsx8cYkfrhOH1G9Pc7u8mC692e3Xu9niJyIV9zk8ZtgCfdCaym53v6_rWvNQikB7RtaxjeSgvThR_oZqzjwQB-YKlV0XKQwF8aqi4jXDopDcBZZGBVTACxKvtwdwkbfEHTlB-GHCDlWogUqyiDJe4WkWpw5mgKUymDhzX6nsrnjPHhDGSTRXHjDny_VxXRsFInAEjbi1yCMKobUaU62fpGIeFnFjRZUMbaI1SJtGyXsIuQcRDcodafOgG_qpMpj44YQFA6aa2vBn42CJfQWxASksfJ7YS5TtMOIMkshaZhBxoZFKH0OM-8gTohvwbd_aUJNU0Thg5ZwxjxrLHWiTmft4XY_4MgzxfDFzNZq2NO_ubxvfoGa-fMxa6Hhkp8WnLfPSkMefN7CGt5CXFxarrYyXvTYCXLDGcskfSp-2-ozxCkOjteb4h81iiBsOcUzskcsC62RbBJpnXenxaij3UbC1OrE6rexLIw0NvUp3pqdulIZyEL8TUNsTB6OxpCil9dYoY43LIz-7iGtda53Mi8GxyjaZ_5gIVE86JFDAiGtUwjsk4goT4SfJDayI2XAURVx8ZVQ9rMhKpLgnpuKXlNFhm5JJsCHuPQ01fiVxJqT8R75Cch9TmQhD3FHOQNwdeSZu_-y8NxkNhoPBuD8eng0nHbIl7qDfOx9OJuPBWX_8ftIfj9IOeclTvuuNz5EAbxUj1efil5z_mdM_eDVT6w)


### Core Models

- Contact

Stores the gallery’s/owner’s public contact info (address lines, city, zip, phone, email, curator details, opening hours).
Useful for rendering the Contact page/footer and for admin updates.
Admin can manage a single or multiple contact records.

- Messages

Captures incoming messages from visitors: name, email, optional phone, message body, subject (general/artwork/exhibition), timestamp.
Links to:
sender: optional authenticated user who submitted it.
owner: the site owner/admin user who should receive/handle it.
Tracks unread state to show counts in the UI and inbox.
Enables listing, filtering, marking as read, and replying workflows.

- MessageReply

Stores replies to a given message with body, timestamp, and who replied (sender is a user).
via_email indicates if the reply was sent out via email (for anonymous visitors) or kept internal (for registered users).
Enables threaded conversation history per message.

#### Typical operations unlocked:

- Display and update official contact information in admin.
- Public contact form submissions create Messages.
- Owner dashboard can:
See unread counts, list messages, filter by subject.
Open a message, mark as read/unread.
Post replies; optionally send via email to non-logged-in senders.
View full reply thread per message.

####  Models

```python
class ArtistProfile(models.Model):
    # Unique ID (auto PK by Django)
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=30, blank=True)
    bio = models.TextField(blank=True)
    image = CloudinaryField(resource_type='image', blank=True, null=True)

    def __str__(self):
        return f"{self.name} <{self.email}>"


class Contact(models.Model):
    address_line_1 = models.CharField(max_length=200)
    address_line_2 = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=20)
    phone = models.CharField(max_length=30)
    email = models.EmailField()
    curator_name = models.CharField(max_length=200, blank=True)
    curator_email = models.EmailField(blank=True)
    opening_hours = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.city} <{self.email}>"
 
```


---

## Testing

### Manual Testing Results

| Test Case                  | Expected Result              | Actual Result | Status |
| -------------------------- | ---------------------------- | ------------- | ------ |
| Click Home menu            | Navigate to homepage         | ✅ Success    | PASS   |
| Click Register             | Open registration form       | ✅ Success    | PASS   |
| Click Login                | Open login form              | ✅ Success    | PASS   |
| Click Logout               | User logged out successfully | ✅ Success    | PASS   |
| Put item in a basket       | Item is in a basket          | ✅ Success    | PASS   |
| Register new account       | Account created successfully | ✅ Success    | PASS   |
| Access admin interface     | Admin panel accessible       | ✅ Success    | PASS   |
| Responsivity               | Works on all devices         | ✅ Success    | PASS   |

**Test Coverage:**

- ✅ Home page loads successfully
- ✅ About and Shop page loads successfully
- ✅ User authentication flows
- ✅ CRUD operations for Artworks

### Code Validation

#### HTML Validation

- **Tool**: [W3C Markup Validation Service](https://validator.w3.org/)
- **Result**: Minor template-related warnings (Django syntax)

#### CSS Validation

- **Tool**: [W3C CSS Validation Service](link)
- **Result**: ✅ No errors found - [CSS Validation](link)

#### Python Validation

- **Tool**: [CI Python Linter](https://pep8ci.herokuapp.com/)
- **Result**: ✅ PEP8 compliant, no errors found

### Lighthouse Performance Testing

[Mobile View Link](https://github.com/DylanAustin-TheDreamer/const-collection-full-stack-hackathon/blob/main/staticfiles/collections_app/images/readme-images/Mobile.png)

**Performance Metrics:**



[Desktop View Link](https://github.com/DylanAustin-TheDreamer/const-collection-full-stack-hackathon/blob/main/staticfiles/collections_app/images/readme-images/Desk.png)

**Performance Metrics:**


---

## Deployment

### Heroku Deployment Process

The site is deployed to **[Heroku](https://www.heroku.com/)** with continuous deployment from the main branch.

#### Deployment Steps

1. **Create Heroku App**
   - Create new "const-collection" app on Heroku dashboard
   - Note the app name for later configuration

2. **Configure Environment Variables**
   - Navigate to app Settings → "Reveal Config Vars"
   - Add all required environment variables:
     - `DATABASE_URL` - PostgreSQL connection string
     - `SECRET_KEY` - Django secret key
     - `CLOUDINARY_URL` - Cloudinary API configuration

3. **Prepare Project Files**
   - Create a `Procfile` with: `web: gunicorn project_name.wsgi`
   - Ensure `Debug = False` in `settings.py`
   - Add `'localhost'` and `'project_name.herokuapp.com'` to `ALLOWED_HOSTS`
   - Update `requirements.txt` with all dependencies

4. **Database Setup**
   - **Service**: PostgreSQL from Code Institute
   - Copy DATABASE_URL from dashboard
   - Add DATABASE_URL to both Heroku Config Vars and local `env.py`
   - Run migrations:
     ```bash
     python3 manage.py makemigrations
     python3 manage.py migrate
     ```

5. **Deploy Application**
   - Connect GitHub repository to Heroku
   - Enable automatic deploys from main branch
   - Perform initial manual deploy
   - Verify deployment success

**Live Application**: [Art of Cecilia](https://const-collection-0f06bd9d4705.herokuapp.com)

---

## AI Integration

GitHub Copilot helped shape user stories, generate Django scaffolding, and streamline frontend design. It also supported error fixes, performance tuning, and deployment.

---

## Credits and Acknowledgements

### Project Foundation

- **[Const Collection Art by Cecilia K.](https://constcollection.com)** -  project provided main inspiration
- **[Django Documentation](https://docs.djangoproject.com/)** - Comprehensive framework guidance
- **[Bootstrap Documentation](https://getbootstrap.com/docs/)** - UI component implementation

### Development Resources and Tools

- **[GitHub Copilot](https://github.com/features/copilot)** - AI-assisted development
- **[Favicon.io](https://favicon.io/favicon-converter/)** - Favicon generation
- **[Shields.io](https://shields.io/)** - README badges
- **[MermaidChart](https://www.mermaidchart.com/)** - Database diagram creation

### Content Sources and Media Attribution

- **[Cloudinary](https://cloudinary.com/)** - Image hosting and optimization

> **Note**: All images are property of Cecilia K. and https://constcollection.com/ website.

---

### Features Left to Implement

- Implement user story: As a visitor, I want to access press articles and academic credentials so I can learn more about the artist’s professional identity.
- Implement user story: A user dashboard displays account info and saved (featured) items.
- Improve performance metrics.

---

<details>
<summary> <strong>Project Specifications</strong></summary>

### Custom Model Implementation


### Technical Achievements

- **Responsive Design**: Mobile-first approach with Bootstrap 5
- **Accessibility**: WCAG compliant with semantic HTML

### Deployment Features

- **Continuous Deployment**: Heroku integration with GitHub
- **Environment Management**: Secure configuration variables
- **Static File Handling**: WhiteNoise for production efficiency
- **Database**: PostgreSQL with Heroku hosting

</details>


<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?logo=django&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-7952B3?logo=bootstrap&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?logo=css3&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=black)
![Heroku](https://img.shields.io/badge/Heroku-430098?logo=heroku&logoColor=white)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-336791?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Badges by Shields.io](https://img.shields.io/badge/Badges-by%20Shields.io-brightgreen?logo=shieldsdotio)](https://shields.io/)
[![Using MermaidChart](https://img.shields.io/badge/Using-MermaidChart-00BFA5?logo=mermaid&logoColor=white)](https://www.mermaidchart.com/)

</div>

