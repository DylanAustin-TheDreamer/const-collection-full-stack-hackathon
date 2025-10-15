# Art by Cecilia

This art gallery project builds upon the evocative foundation laid by Cecilia K’s Evening Garden Exhibition, expanding its message into a multi-sensory, interactive experience. The original work is a quiet revolution—a call to reclaim feminine identity, ancestral wisdom, and embodied truth in a world of digital distortion and performative culture. Our enhanced version seeks to deepen this narrative by blending visual storytelling, ambient soundscapes, and immersive design to create a sanctuary of reflection and reconnection.



This platform is designed to honor the artist's voice, showcase their evolving body of work, and invite visitors into a space of emotional resonance and thoughtful exploration. It blends storytelling, visual clarity, and intuitive navigation to serve artists, visitors, and buyers alike.

<br>

<p align="center">
    <a href="https://constcollection.com/" target="_blank" rel="noopener noreferrer">
        <img src="https://github.com/DylanAustin-TheDreamer/const-collection-full-stack-hackathon/blob/main/collections_app/static/collections_app/images/readme-images/Cecilia.png" alt="Art by Cecilia" style="max-width:100%;height:auto;">
    </a>
    <br>
    <em>Artwork: Art by Cecilia K. — <a href="https://constcollection.com/" target="_blank" rel="noopener noreferrer">constcollection.com</a></em>
</p>

 **Deployed Link**: [Art by Cecilia](link will be here)

---

## Table of Contents

1. [Features](#features)
   - [Existing Features](#existing-features)
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
3. [User Stories & Planning](#user-stories--planning)
4. [Database Design](#database-design)
   - [ERD Diagram](#erd-diagram)
   - [Core Models](#core-models)
5. [Testing](#testing)
   - [Manual Testing Results](#manual-testing-results)
   - [Code Validation](#code-validation)
   - [Lighthouse Performance Testing](#lighthouse-performance-testing)
6. [Deployment](#deployment)
   - [Heroku Deployment Process](#heroku-deployment-process)
   - [Deployment Steps](#deployment-steps)
7. [AI Integration](#-ai-integration)
8. [Credits and Acknowledgements](#credits-and-acknowledgements)
   - [Project Foundation](#project-foundation)
   - [Development Resources and Tools](#development-resources-and-tools)
   - [Content Sources and Media Attribution](#content-sources-and-media-attribution)
9. [Features Left to Implement](#features-left-to-implement)
10. [Known Bugs, To Be Fixed](#known-bugs-to-be-fixed)
11. [Project Specifications](#project-specifications)

---

## Features

### Core Functionality

- **Home Page**  responsive design [Here](githublink)
- **Picture Detail Pages** - Complete race information with comments system [Here](githublink)
- **User Authentication** - Register, login, logout functionality, Password Reset [Here](githublink)
- **Picture Management** - Create, read, update, and delete races (CRUD) [Here](githublink)


#### User Experience

- **Responsive Design** - Works perfectly on all devices [Here](githublink)
- **Modern UI** - Clean, accessible interface with Bootstrap 5
- **Fast Loading** - Optimized images and performance enhancements 
- **Image Upload** - Cloudinary integration for images

#### Administrative Features

- **Admin Interface** - Full Django admin for content management

### Wireframes

## [Wireframes](http://bit.ly/43f0FE9)

### Color Scheme

Minimalist Palette Philosophy
This grayscale palette—ranging from pure white to absolute black—embodies the principles of minimalism: clarity, restraint, and emotional space. It serves as a neutral canvas that allows the artwork to speak without distraction, letting color-rich pieces radiate with full intensity.

Name	Hex Code	Usage Suggestion
Pure White	#FFFFFF	Background, whitespace, clean canvas
Light Gray	#F5F5F5	Section dividers, subtle hover effects
Cool Gray	#D3D3D3	Card backgrounds, secondary text
Medium Gray	#A9A9A9	Borders, muted buttons
Charcoal Gray	#555555	Body text, icons
Graphite	#333333	Headings, navigation bar
Absolute Black	#000000	Accent text, high-contrast elements

![Color Palette](https://github.com/DylanAustin-TheDreamer/const-collection-full-stack-hackathon/blob/main/collections_app/static/collections_app/images/readme-images/palette-white-black.png)

### Typography

The site uses **Google Fonts**

### Imagery

- **Source**: [Art by Cecilia K.](https://constcollection.com/)
- **Hosting**: [Cloudinary](https://cloudinary.com/) for optimized loading
- **Optimization**: Responsive images with proper aspect ratios
- **Performance**: Lazy loading and fetchpriority for critical images

---

## Technologies Used

### Backend

- **[Python 3.12](https://www.python.org/)** - Core programming language
- **[Django 4.2](https://www.djangoproject.com/)** - Web framework
- **[PostgreSQL](https://www.postgresql.org/)** - Database system
- **[Django Allauth](https://django-allauth.readthedocs.io/)** - Authentication system

### Frontend

- **[HTML5](https://developer.mozilla.org/en-US/docs/Web/HTML)** - Markup language
- **[CSS3](https://developer.mozilla.org/en-US/docs/Web/CSS)** - Styling
- **[JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)** - Interactive functionality
- **[Bootstrap 5](https://getbootstrap.com/)** - CSS framework
- **[Font Awesome](https://fontawesome.com/)** - Icons
- **[Google Fonts](https://fonts.google.com/)** - Typography (Inter & Lato)

### Cloud Services & Deployment

- **[Heroku](https://www.heroku.com/)** - Application hosting
- **[Cloudinary](https://cloudinary.com/)** - Image hosting and optimization
- **[WhiteNoise](https://whitenoise.evans.io/)** - Static file serving

### Development Tools

- **[GitHub](https://github.com/)** - Version control
- **[GitHub Copilot](https://github.com/features/copilot)** - AI-assisted development
- **[VS Code](https://code.visualstudio.com/)** - Code editor
- **[Chrome DevTools](https://developer.chrome.com/docs/devtools/)** - Testing and debugging

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

- Platform Essentials
Simple Navigation Bar Clear links to Home, Gallery, Exhibitions, About Me, and Contact.

-- Mobile Responsiveness Seamless viewing across devices.

- Social Media Integration Visitors can follow the artist’s journey on Instagram, Facebook, and YouTube.

####  Models

```python
class 
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
- ✅ Detail page loads successfully
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

[Mobile View Link](link)

**Performance Metrics:**



[Desktop View Link](link)

**Performance Metrics:**


---

## Deployment

### Heroku Deployment Process

The site is deployed to **[Heroku](https://www.heroku.com/)** with continuous deployment from the main branch.

#### Deployment Steps

1. **Create Heroku App**
   - Create new "run-for-fun" app on Heroku dashboard
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

**Live Application**: [Art of Cecilia](link)

---

## AI Integration

GitHub Copilot helped shape user stories, generate Django scaffolding, and streamline frontend design. It also supported error fixes, performance tuning, and deployment with WhiteNoise and Cloudinary.

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


---

### Known bugs, to be fixed


---

<details>
<summary> <strong>Project Specifications</strong></summary>

### Custom Model Implementation


### Technical Achievements

- **Responsive Design**: Mobile-first approach with Bootstrap 5
- **Accessibility**: WCAG compliant with semantic HTML
- **Security**: CSRF protection and secure authentication

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

