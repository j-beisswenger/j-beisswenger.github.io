import yaml
from collections import defaultdict
import bibtexparser

class WebsiteCreator:
    def __init__(self):
        self.read_profile_data()
        self.generate_awards_section()
        self.read_authors()
        self.generate_publications_section()

    def read_profile_data(self):
        with open('profile.yaml', 'r') as yaml_file:
            data = yaml.load(yaml_file, Loader=yaml.FullLoader)
            self.first_name = data['First name']
            self.surname = data['Surname']
            self.name = self.first_name + ' ' + self.surname
            self.title = data['Title']
            self.bio = data['Bio']
            self.cv = data['CV']
            self.mail = data['Mail']
            self.scholar = data['Scholar']
            self.github = data['GitHub']
            self.linkedin = data['LinkedIn']
            self.youtube = data['YouTube']

    def read_authors(self):
        with open('authors.yaml', 'r') as yaml_file:
            self.authors = yaml.load(yaml_file, Loader=yaml.FullLoader)

    def generate_awards_section(self):
        self.awards = ""

        with open('awards.yaml', 'r') as yaml_file:
            awards = yaml.load(yaml_file, Loader=yaml.FullLoader)

            for award in awards:
                data = defaultdict(str)
                templates = {
                    'Date': """<p class="award-date">TODO</p>""",
                    'Title': """<h4 class="award-title">TODO</h4>""",
                    'Project Page': """<a href="TODO" target="_blank"><i class="fas fa-globe"></i> Project Page</a>""",
                    'Organizer': """<p class="award-organizer">TODO</p>""",
                    'Description': """<a href="#" onclick="toggleDescription(this)"><i class="fas fa-book-open"></i> Description</a>""",
                    'Code': """<a href="TODO" target="_blank"><i class="fas fa-code"></i> Code</a>""",
                }

                for key, value in templates.items():
                    if key in award:
                        data[key] = value.replace('TODO', award[key])
                
                description = ""
                description_button = ""
                if 'Description' in award:
                    description_button = """<a href="#" onclick="toggleDescription(this)"><i class="fas fa-book-open"></i> Description</a>"""
                    description = f"""
                        <p class="award-description">
                        {award['Description']}
                        </p>
                    """

                self.awards += f"""
                    <div class="award-item row mb-3 p-2 rounded">
                        <div class="award-header">
                            {data['Date']}
                            {data['Title']}
                        </div>
                            {data['Organizer']}
                            <div class="publication-links">
                            {data['Project Page']}
                            {data['Code']}
                            {description_button}
                        </div>
                        {description}
                    </div>
                    """

    def generate_publications_section(self):
        self.publications = ""

        with open('publications.bib', 'r') as f:
            bib_database = bibtexparser.load(f)
            for entry in bib_database.entries:
                data = defaultdict(str)

                templates = {
                    'img': """<img src="TODO" class="publication-img img-fluid rounded">""", 
                    'pdf': """<a href="TODO" target="_blank"><i class="fas fa-file-pdf"></i> Paper</a>""", 
                    'html': """<a href="TODO" target="_blank"><i class="fas fa-globe"></i> Project Page</a>""", 
                    'award': """<span class="badge bg-danger mb-3">TODO</span>""", 
                    'code': """<a href="TODO" target="_blank"><i class="fas fa-code"></i> Code</a>""",
                    'booktitle': """<p><i>BOOKTITLE, YEAR</i></p>""", 
                    'title': """<h3 class="mt-3 mt-md-0 mb-3">TODO</h3>""",
                    'video': """<a href="TODO" target="_blank"><i class="fab fa-youtube"></i> Video</a>""",
                }

                for key, value in templates.items():
                    if key in entry:
                        data[key] = value.replace('TODO', entry[key])

                if 'booktitle' in entry or 'year' in entry:
                    data['booktitle'] = '<p><i>'
                    data['booktitle'] += entry['booktitle'] if 'booktitle' in entry else ''
                    data['booktitle'] += ', ' if 'booktitle' in entry and 'year' in entry else ''
                    data['booktitle'] += entry['year'] if 'year' in entry else ''
                    data['booktitle'] += '</i></p>'

                if 'author' in entry:
                    authors = entry['author'].split(', ')
                    l = []
                    for author in authors:
                        if author == self.name:
                            l.append(f'<strong>{author}</strong>')
                        elif author in self.authors:
                            l.append(f"""<a href="{self.authors[author]}" class="author-hyperref">{author}</a>""")
                        else:
                            l.append(author)

                    author_string = ', '.join(l)
                    data['author'] = f"""
                        <p><strong>Authors:</strong> {author_string}</p>
                        """

                bibtex_button, bibtex = "", ""
                if 'bibtex' in entry:
                    l = []
                    for key in entry['bibtex'].split(', '):
                        l.append(f"    {key} = {{{entry[key]}}}")
                    entries = '\n'.join(l)
                    bibtex = f"""@{entry['ENTRYTYPE']}{{{entry['ID']},\n{entries}\n}}"""
                    bibtex_button = """<a href="#" id="toggle-bibtex" onclick="toggleBibtex(event)"><i class="fas fa-quote-right"></i> Bibtex</a>"""

                abstract, abstract_button = "", ""
                if 'abstract' in entry:
                    abstract_button = f"""<a href="#" class="toggle-abstract" onclick="toggleAbstract(event)"><i class="fas fa-book-open"></i> Abstract</a>"""
                    abstract = entry['abstract']

                self.publications += fr"""
                    <div class="publication-item row mb-4 p-4 rounded">
                        <div class="col-md-3">
                            {data['img']}
                        </div>
                        <div class="col-md-9">
                            {data['title']}
                            {data['award']}
                            {data['author']}
                            {data['booktitle']}
                            
                            <div class="publication-links">
                                {data['pdf']}
                                {data['html']}
                                {data['code']}
                                {data['video']}
                                {abstract_button}
                                {bibtex_button}
                            </div>

                            <div class="hidden-content abstract-section" style="display: none;">
                                <p>{abstract}</p>
                            </div>

                            <div class="hidden-content bibtex-section" style="display: none;">
                                <div class="bibtex-header">
                                <pre class="bibtex-content">
{bibtex}</pre>
                                <button class="btn btn-secondary btn-sm copy-bibtex" onclick="copyBibtex(this)">Copy Bibtex</button>
                                </div>
                            </div>
                        </div>
                    </div>
                    """

    def _generate_website(self):
        return fr"""<!doctype html>
<html lang="en">

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <meta name="description"
    content="Personal website of {self.name}, {self.title}">

  <title>{self.name} - Machine Learning Researcher</title>
  <link rel="icon" type="image/x-icon" href="assets/favicon.ico">

  <!-- Bootstrap CSS -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css">
  <!-- Font Awesome -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <!-- Google Fonts -->
  <link
    href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&family=Playfair+Display:wght@700&display=swap"
    rel="stylesheet">

  <style>
    :root {{
      --primary-color: #2c3e50;
      --secondary-color: #3498db;
      --accent-color: #e74c3c;
      --text-color: #333333;
      --bg-color: #f5f5f5;
      --dark-bg: #1a1a2e;
      --dark-text: #e0e0e0;
      --dark-nav: #34495e;
      --dark-mode-heading: #c8dded;
    }}

    section {{
      scroll-margin-top: 96px; /* Adjust this value based on your header height */
    }}

    #awards .award-header {{
      display: flex;             /* Align date and title horizontally */
      align-items: baseline
    }}

    #awards .award-title {{
      font-weight: bold;         /* Bold font for the title */
      margin: 0;                 /* Remove extra space around the title */
    }}

    #awards .award-item {{
      transition: transform 0.3s ease, box-shadow 0.3s ease;
      border: none;
      border-radius: 15px;
      overflow: hidden;
      background-color: #ffffff;
      line-height: 1.5;
    }}

    #awards .award-item:hover {{
      transform: translateY(-5px);
      box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }}

    #awards h4 {{
      color: var(--primary-color);
      margin-bottom: 5px;
      font-size: 1.2rem;
    }}

    #awards .award-date {{
      font-weight: bold;
      margin-right: 15px;        /* Add space between the date and title */
      font-size: 0.9em;          /* Smaller font size for the date */
      color: var(--secondary-color);
      margin-bottom: 5px;
      color: #1f486f
    }}

    #awards .award-organizer {{
      font-style: italic;
      margin-bottom: 10px;
    }}

    #awards .award-buttons {{
      display: flex;
      justify-content: space-between;
      margin-top: 10px;
    }}

    #awards .award-button {{
      padding: 6px 12px;
      /* Reduced from 8px 16px */
      border: 1px solid var(--primary-color);
      background-color: transparent;
      color: var(--primary-color);
      border-radius: 5px;
      cursor: pointer;
      transition: background-color 0.3s ease, color 0.3s ease;
    }}

    #awards .award-button:hover {{
      background-color: var(--primary-color);
      color: #ffffff;
    }}

    #awards .award-description {{
      display: none;
      margin-top: 10px;
      /* Reduced from 15px */
      font-size: 0.9rem;
      line-height: 1.4;
      /* Reduced from 1.5 */
    }}

    body.dark-mode #awards .award-item {{
      background-color: #103252;
    }}

    body.dark-mode #awards h4 {{
      color: var(--dark-mode-heading);
    }}

    body.dark-mode #awards .award-button {{
      border-color: var(--dark-text);
      color: var(--dark-text);
    }}

    body.dark-mode #awards .award-button:hover {{
      background-color: var(--dark-text);
      color: var(--dark-bg);
    }}

    body.dark-mode #awards .award-date {{
      color: #81a6c8
    }}

    .futuristic-profile {{
      /* background: #e74141f3; */
      /* backgrorgb(67, 83, 98)or: #11b71700; */
      border-radius: 20px;
      padding: 2rem;
      /* box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1); */
      color: var(--text-color);
    }}

    .profile-header {{
      margin-left: auto;
      margin-right: auto;
      /*text-align: center;  Center the content */
    }}

    .profile-img {{
      position: relative;
      max-width: 240px;
      border-radius: 50%;
      /* border: 5px solid white;  */
      overflow: hidden;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
      transition: all 0.3s ease;
      margin: 0 auto;
      /* Center the image */
      display: block;
      /* Ensure it takes full width */
    }}

    .profile-img:hover {{
      transform: scale(1.05);
    }}

    .profile-name {{
      font-size: 2.5rem;
      margin-bottom: 0.5rem;
      background: var(--primary-color);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}

    .profile-title {{
      font-size: 1.2rem;
      opacity: 0.8;
    }}

    .section-title {{
      font-size: 1.8rem;
      margin-bottom: 1rem;
      position: relative;
      display: inline-block;
      color: var(--primary-color);
    }}

    .section-title::after {{
      content: '';
      position: absolute;
      bottom: -5px;
      left: 0;
      width: 50%;
      height: 3px;
      background: var(--accent-color);
    }}

    .about-me p {{
      margin-bottom: 1rem;
      line-height: 1.6;
    }}

    @media (max-width: 768px) {{
      .futuristic-profile {{
        border-radius: 0;
      }}
    }}

    body {{
      font-family: 'Roboto', sans-serif;
      background-color: var(--bg-color);
      color: var(--text-color);
      transition: background-color 0.3s ease, color 0.3s ease;
      line-height: 1.8;
      padding-top: 76px;
    }}

    .navbar {{
      background-color: var(--primary-color);
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
      padding: 1rem 0;
    }}

    .navbar-brand {{
      font-family: 'Playfair Display', serif;
      font-size: 1.5rem;
      color: var(--bg-color) !important;
    }}

    .navbar-nav .nav-link {{
      font-weight: 500;
      text-transform: uppercase;
      letter-spacing: 1px;
      padding: 0.5rem 1rem;
      color: var(--bg-color) !important;
    }}

    .navbar-nav .nav-item:last-child {{
      margin-left: 10px;
    }}

    #darkModeToggle {{
      background: none;
      border: none;
      color: var(--bg-color);
      font-size: 1.2rem;
      padding: 0;
      transition: color 0.3s ease;
    }}

    #darkModeToggle:hover {{
      color: var(--secondary-color);
    }}

    body.dark-mode {{
      color: #d2d8dc;
      background-color: #051429;
    }}

    body.dark-mode #darkModeToggle {{
      color: var(--dark-text);
    }}

    .dark-mode-toggle {{
      display: none;
    }}

    @media (max-width: 992px) {{
      .navbar-nav {{
        padding-top: 10px;
      }}

      .navbar-nav .nav-item:last-child {{
        margin-left: 0;
        margin-top: 10px;
      }}
    }}

    .contact-links {{
      justify-content: center !important;
    }}

    body.dark-mode .contact-links .btn {{
      color: var(--dark-text);
      border-color: var(--dark-text);
    }}

    body.dark-mode .contact-links .btn:hover {{
      background-color: var(--dark-text);
      color: var(--dark-bg);
    }}

    .contact-links .btn {{
      margin: 0.5rem;
      border-radius: 50px;
      transition: all 0.3s ease;
      font-weight: 500;
      padding: 0.5rem 1.5rem;

      color: #1c6ca2;
      border-color: #8d8d8d;
    }}

    .contact-links .btn:hover {{
      transform: translateY(-3px);
      box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);

      color: #1c6ca2;
      background-color: #bebebe;
    }}

    h1,
    h2,
    h3,
    h4,
    h5 {{
      font-family: 'Playfair Display', serif;
      color: var(--primary-color);
    }}

    .publication-item {{
      transition: transform 0.3s ease, box-shadow 0.3s ease;
      border: none;
      border-radius: 15px;
      overflow: hidden;
      background-color: #ffffff;
      box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
    }}

    .publication-item:hover {{
      transform: translateY(-5px);
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
    }}

    .author-hyperref {{
      color: #2180c0;
      text-decoration: none;
      /* Remove underline */
    }}

    body.dark-mode .author-hyperref {{
      color: var(--dark-text);
    }}

    .publication-img {{
      height: 250px;
      object-fit: cover;
      width: 100%;
      height: auto
    }}

    .publication-links a {{
      color: #2180c0;
      /* color: var(--secondary-color); */
      margin-right: 15px;
      text-decoration: none;
      transition: color 0.3s ease;
      font-weight: 500;
    }}

    .dark-mode .publication-links a {{
      color: #4fa3db;
    }}

    .publication-links a:hover {{
      color: var(--accent-color);
    }}

    .hidden-content {{
      background-color: #f1f3f5;
      border-radius: 10px;
      padding: 1.5rem;
      margin-top: 1rem;
      font-size: 0.9rem;
    }}

    footer {{
      background-color: var(--primary-color);
      color: white;
      padding: 10px 0;
      /* Reduce the padding for less space */
      position: fixed;
      bottom: 0;
      width: 100%;
      font-size: 0.9rem;
    }}

    footer p {{
      margin-bottom: 0;
    }}

    footer .social-icons a {{
      color: white;
      margin-left: 0.5rem;
      font-size: 1rem;
    }}

    body.dark-mode .navbar-brand body.dark-mode .navbar-nav .nav-link {{
      color: var(--dark-text) !important;
    }}

    body.dark-mode footer {{
      background-color: #123c5b;
    }}

    body.dark-mode .navbar {{
      background-color: #123c5b;
    }}

    body.dark-mode .publication-item {{
      background-color: #174570;
    }}

    body.dark-mode .hidden-content {{
      background-color: #3a6b9c;
    }}

    body.dark-mode .section-title {{
      color: #bfd1dd
    }}

    body.dark-mode .futuristic-profile {{
      background-color: #45719700;
      color: #d0e0ed;
      height: 10px
    }}

    body.dark-mode .profile-name {{
      background-color: #ffffff;
    }}

    body.dark-mode h1,
    body.dark-mode h2,
    body.dark-mode h3,
    body.dark-mode h4,
    body.dark-mode h5 {{
      color: #d0daea;
    }}

    .dark-mode-toggle {{
      top: 30px;
      right: 20px;
      z-index: 1050;
    }}

    .dark-mode-toggle button {{
      background-color: var(--primary-color);
      color: white;
      border: none;
      width: 50px;
      height: 50px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
      transition: all 0.3s ease;
      padding: 0;
    }}

    .dark-mode-toggle button:hover {{
      background-color: var(--secondary-color);
      transform: scale(1.1);
    }}

    .dark-mode-toggle button i {{
      font-size: 1.2rem;
    }}

    .copy-bibtex {{
      padding: 0.25rem 0.5rem;
      font-size: 0.85rem;
      margin-top: 0.5rem;
    }}

    .dark-mode .copy-bibtex {{
      background-color: #174570;
      border-color: #11b71700;
    }}

    #bibtex-content {{
      font-size: 0.8rem;
      white-space: pre-wrap;
      word-wrap: break-word;
    }}

    .left-column {{
      position: sticky;
      top: 76px;
      /* height of the fixed header */
      height: calc(100vh - 76px - 20px);
      /* 76px for header, 56px for footer */
      overflow-y: hidden;
      /* Enable scrolling if content overflows */
      padding: 20px;
    }}

    .right-column {{
      padding: 20px;
      margin-bottom: 26px;
    }}

    @media (max-width: 768px) {{

      .left-column,
      .right-column {{
        position: static;
        width: 100%;
        margin-left: 0;
      }}
    }}
  </style>
</head>

<body>
  <!-- Navigation Bar -->
  <nav class="navbar navbar-expand-lg fixed-top">
    <div class="container">
      <a class="navbar-brand" href="#awards">{self.name}</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
        aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto align-items-center">
          <li class="nav-item">
            <a class="nav-link" href="#awards">Awards</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#publications">Publications</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#homepage_templage">Design</a>
          </li>
          <li class="nav-item">
            <button id="darkModeToggle" class="btn btn-link nav-link" aria-label="Toggle dark mode">
              <i class="fas fa-moon"></i>
            </button>
          </li>
        </ul>
      </div>
    </div>
  </nav>
  <div class="container-fluid">
    <div class="row">
      <!-- Left Column (Sticky) -->
      <div class="col-md-4 left-column">
        <!-- Profile Section -->
        <section id="about" class="futuristic-profile">
          <div class="profile-header">
            <div class="col-md-12 col-lg-12 text-center mb-1">
              <img src="assets/profile.jpg" class="profile-img img-fluid mb-3" alt="{self.name}">
            </div>
            <h1 class="profile-name">
              {self.name}
            </h1>
            <p class="profile-title">
              {self.title}
            </p>
          </div>

          <div class="contact-links d-flex flex-wrap justify-content-center">
            <a href="{self.cv}" target="_blank" class="btn btn-outline-primary">
              <i class="fa fa-address-card" aria-hidden="true"></i> CV
            </a>
            <a href="mailto:{self.mail}" class="btn btn-outline-primary">
              <i class="far fa-envelope-open" aria-hidden="true"></i> Mail
            </a>
            <a href="{self.scholar}" target="_blank"
              class="btn btn-outline-primary">
              <i class="fa-solid fa-book" aria-hidden="true"></i> Scholar
            </a>
            <a href="{self.github}" target="_blank" class="btn btn-outline-primary">
              <i class="fab fa-github" aria-hidden="true"></i> Github
            </a>
            <a href="{self.linkedin}" target="_blank" class="btn btn-outline-primary">
              <i class="fab fa-linkedin" aria-hidden="true"></i> LinkedIn
            </a>
            <a href="{self.youtube}" target="_blank" class="btn btn-outline-primary">
              <i class="fab fa-youtube" aria-hidden="true"></i> YouTube
            </a>
          </div>

          <!-- Bio & Interests -->
          <section class="about-me">
            <h2 class="section-title">About Me</h2>
            <p>{self.bio}</p>
          </section>
          </section>
      </div>
      <!-- Right column remains unchanged -->
      <!-- </div> -->
      <!-- </div> -->

      <!-- Right Column (Scrollable) -->
      <div class="col-md-8 right-column">
        <!-- Awards Section -->

        <section id="awards">
          <h2 class="section-title mb-4">Awards</h2>
          {self.awards}
          
          

        </section>

        <!-- Publications Section -->
        <section id="publications">
          <h2 class="section-title mb-4">Publications</h2>
          {self.publications}
        </section>

        <section id="homepage_templage">
          <h2 class="section-title mb-4">Homepage Template</h2>
          <p>This website's design is inspired by <a href="https://m-niemeyer.github.io/" target="_blank"
              class="author-hyperref">Michael
              Niemeyer's personal site</a>. Checkout his <a href="https://github.com/m-niemeyer/m-niemeyer.github.io"
              target="_blank" class="author-hyperref">GitHub</a>!</p>
        </section>
      </div>
    </div>

  </div>

  <!-- Footer -->
  <footer class="py-2">
    <div class="container">
      <div class="row align-items-center">
        <div class="col-md-6 text-center text-md-start">
        </div>
        <div class="col-md-6 text-center text-md-end social-icons">
          <!-- <a href="#" class="text-white"><i class="fab fa-twitter"></i></a> -->
          <a href="{self.github}" class="text-white"><i class="fab fa-github"></i></a>
          <a href="{self.linkedin}" class="text-white"><i class="fab fa-linkedin"></i></a>
        </div>
      </div>
    </div>
  </footer>

  <!-- Dark Mode Toggle -->
  <div class="dark-mode-toggle">
    <button id="darkModeToggle" class="btn" aria-label="Toggle dark mode">
      <i class="fas fa-moon"></i>
    </button>
  </div>

  <!-- Bootstrap JS -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/js/bootstrap.bundle.min.js"></script>

  <!-- Custom Scripts -->
  <script>
    document.addEventListener('DOMContentLoaded', (event) => {{
      const darkModeToggle = document.getElementById('darkModeToggle');
      const body = document.body;
      const icon = darkModeToggle.querySelector('i');

      // Check for saved theme preference or default to light mode
      const savedTheme = localStorage.getItem('theme');
      if (savedTheme === 'dark') {{
        body.classList.add('dark-mode');
        icon.classList.replace('fa-moon', 'fa-sun');
      }}

      darkModeToggle.addEventListener('click', () => {{
        body.classList.toggle('dark-mode');
        const isDarkMode = body.classList.contains('dark-mode');
        localStorage.setItem('theme', isDarkMode ? 'dark' : 'light');

        if (isDarkMode) {{
          icon.classList.replace('fa-moon', 'fa-sun');
        }} else {{
          icon.classList.replace('fa-sun', 'fa-moon');
        }}
      }});
    }});

    function toggleAbstract(event) {{
      event.preventDefault();
      const publicationItem = event.target.closest('.publication-item');
      const abstractSection = publicationItem.querySelector('.abstract-section');
      abstractSection.style.display = abstractSection.style.display === 'none' ? 'block' : 'none';
      const bibtexSection = publicationItem.querySelector('.bibtex-section');

      if (abstractSection.style.display === 'block') {{
        bibtexSection.style.display = 'none';
      }}
    }}

    function toggleBibtex(event) {{
      event.preventDefault();
      const publicationItem = event.target.closest('.publication-item');
      const bibtexSection = publicationItem.querySelector('.bibtex-section');
      bibtexSection.style.display = bibtexSection.style.display === 'none' ? 'block' : 'none';
      const abstractSection = publicationItem.querySelector('.abstract-section');

      if (bibtexSection.style.display === 'block') {{
        abstractSection.style.display = 'none';
      }}
    }}

    function copyBibtex(button) {{
      const bibtexContent = button.previousElementSibling.textContent;
      navigator.clipboard.writeText(bibtexContent)
        .then(() => {{
          button.textContent = 'Copied!';
          setTimeout(() => {{
            button.textContent = 'Copy Bibtex';
          }}, 2000);
        }})
        .catch(err => {{
          console.error('Failed to copy: ', err);
        }});
    }}

    function toggleDescription(button) {{
      const description = button.parentElement.nextElementSibling;
      if (description.style.display === 'none' || description.style.display === '') {{
        description.style.display = 'block';
      }} else {{
        description.style.display = 'none';
      }}
    }}

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
      anchor.addEventListener('click', function (e) {{
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({{
          behavior: 'smooth'
        }});
      }});
    }});
  </script>

</body>

</html>
"""

    def save_website(self):
        website = self._generate_website()

        with open('index.html', 'w') as f:
            f.write(website)

if __name__ == '__main__':
    WebsiteCreator().save_website()