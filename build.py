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
                    <div class="award-item row mb-3 p-2">
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
                  <div class="publication-item row mb-3 p-2">
                    <div class="image-container col-md-3">
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
        return fr"""<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{self.name} - Machine Learning Researcher</title>

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
    }}

    body,
    html {{
      font-family: 'Roboto', sans-serif;
      margin: 0;
      padding: 0;
      height: 100%;
      font-family: Arial, sans-serif;
      overflow: hidden;
      --accent-color: #e74c3c;
      --dark-nav: #34495e;
      --bg-color: #f5f5f5;
      --header-color: #2d3e4f;
      --dark-text: #e0e0e0;
      background-color: var(--bg-color);
      transition: background-color 0.3s ease, color 0.3s ease;
    }}

    body.dark-mode {{
      background-color: #152331;
      --primary-color: #f7f7f7;
    }}

    body.dark-mode .contact-links .btn {{
      color: var(--dark-text);
      border-color: var(--dark-text);
    }}

    body.dark-mode .contact-links .btn:hover {{
      background-color: var(--dark-text);
      color: var(--dark-bg);
    }}

    .navbar a {{
      color: #f2f2f2;
    }}

    .main {{
      display: flex;
      height: calc(100vh - 103px);
      margin-top: 58px;
    }}

    .left-column {{
      display: flex;
      flex-direction: column;
      width: 33%;
      overflow: hidden;
      padding: 2.0rem 2.0rem;
    }}

    .navbar {{
      background-color: var(--dark-nav);
      z-index: 1000;
      height: 58px;
      max-height: 56px;
    }}

    .navbar-brand {{
      font-family: 'Playfair Display', serif;
      font-size: 1.5rem;
      color: var(--bg-color) !important;
    }}

    .navbar-nav .nav-link {{
      font-family: 'Roboto', sans-serif;
      text-transform: uppercase;
      letter-spacing: 1px;
      padding: 0.5rem 1rem;
      color: var(--bg-color) !important;
    }}

    .award-header {{
      display: flex;
      align-items: baseline
    }}

    #awards h4 {{
      color: var(--primary-color);
      margin-bottom: 5px;
      font-size: 1.2rem;
    }}

    #awards .award-date {{
      font-weight: bold;
      margin-right: 15px;
      font-size: 0.9em;
      color: #1f486f;
      margin-bottom: 5px;
    }}

    #awards .award-organizer {{
      font-style: italic;
      margin-bottom: 10px;
      color: var(--primary-color)
    }}

    #awards .award-buttons {{
      display: flex;
      justify-content: space-between;
      margin-top: 10px;
    }}

    #awards .award-button {{
      padding: 6px 12px;
      border: 1px solid var(--primary-color);
      background-color: transparent;
      color: var(--primary-color);
      border-radius: 5px;
      cursor: pointer;
      transition: background-color 0.3s ease, color 0.3s ease;
    }}

    .publication-links a {{
      color: #2180c0;
      margin-right: 15px;
      text-decoration: none;
      transition: color 0.3s ease;
      font-weight: 500;
    }}

    body.dark-mode .publication-links a {{
      color: #66b3e7;
    }}

    .publication-links a:hover {{
      color: var(--accent-color);
    }}

    #awards .award-button:hover {{
      background-color: var(--primary-color);
      color: #ffffff;
    }}

    #awards .award-description {{
      color: var(--primary-color);
      display: none;
      margin-top: 10px;
      font-size: 0.9rem;
      line-height: 1.4;
    }}

    .award-title {{
      font-family: 'Playfair Display', serif;
      font-weight: bold;
      margin: 0;
    }}

    .hidden-content {{
      background-color: #f1f3f5;
      color: var(--primary-color);
      border-radius: 10px;
      padding: 1.5rem;
      margin-top: 1rem;
      font-size: 0.9rem;
    }}

    body.dark-mode .hidden-content{{
      background-color: #0d2135;
    }}

    #awards .award-item {{
      transition: transform 0.3s ease, box-shadow 0.3s ease;
      border: none;
      overflow: hidden;
      background-color: #ffffff;
      line-height: 1.5;
      border-radius: 10px;
      margin-right: 1rem;
    }}

    body.dark-mode #awards .award-item {{
      background-color: #1d3954;
    }}

    body.dark-mode #publications .publication-item {{
      background-color: #1d3954;
      color: var(--primary-color);
    }}

    #awards .award-item:hover {{
      transform: translateY(-5px);
      box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
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
      transition: all 0.3s ease;
    }}

    .profile-img {{
      height: 30%;
      width: auto;
      border-radius: 50%;
      transition: all 0.3s ease;
      margin: 0 auto;
    }}

    .about-me {{
      color: var(--primary-color);
      margin: 0;
      padding: 0;
      flex-grow: 1;
      display: flex;
      justify-content: left;
      align-items: left;
      font-size: 1.7vmin;
      transition: all 0.3s ease;
    }}

    .homepage-template {{
      color: var(--primary-color);
    }}

    .profile-img:hover {{
      transform: scale(1.05);
    }}

    .profile-header {{
      margin-top: 1rem;
      flex-grow: 1;
      display: flex;
      justify-content: left;
      align-items: left;
      font-size: 4vmin;
      transition: all 0.3s ease;
      font-family: 'Playfair Display', serif;
      color: var(--header-color);
      margin: 0;
      padding: 0;
    }}

    body.dark-mode .profile-header {{
      color: var(--dark-text);
    }}

    .about-me-header {{
      flex-grow: 1;
      position: relative;
      display: inline-block;
      font-size: 3vmin;
      font-family: 'Playfair Display', serif;
      color: var(--header-color);
      margin-bottom: 10px;
    }}

    .about-me-header::after {{
      content: '';
      position: absolute;
      left: 0;
      top: 4vmin;
      width: 12%;
      height: 3px;
      background-color: var(--accent-color);
    }}

    #publications .publciations-header,
    #awards .awards-header,
    #homepage_template .homepage-template-header {{
      position: relative;
      display: inline-block;
      font-family: 'Playfair Display', serif;
      margin-bottom: 20px;
      font-size: 3vmin;
      color: var(--header-color)
    }}

    body.dark-mode .about-me-header,
    body.dark-mode #publications .publciations-header,
    body.dark-mode #awards .awards-header,
    body.dark-mode #homepage_template .homepage-template-header {{
      color: var(--dark-text)
    }}

    #publications .publciations-header::after,
    #awards .awards-header::after,
    #homepage_template .homepage-template-header::after {{
      content: '';
      position: absolute;
      left: 0;
      bottom: -3px;
      width: 50%;
      height: 3px;
      background-color: var(--accent-color);
    }}

    #publications h3 {{
      font-family: 'Playfair Display', serif;
    }}

    .profile-title {{
      flex-grow: 1;
      display: flex;
      justify-content: left;
      align-items: left;
      font-size: 2.2vmin;
      transition: all 0.3s ease;
      color: #5a5a5a;
      margin: 0;
      padding: 0;
    }}

    body.dark-mode .profile-title {{
      color: #bbbbbb;
    }}

    body.dark-mode #awards .award-date {{
      color: #bbbbbb;
    }}

    .contact-links {{
      display: flex;
      justify-content: center;
      flex-wrap: wrap;
      font-size: 4vmin;
      transition: all 0.3s ease;
      margin-top: 1.rem;
    }}

    .contact-links a {{
      margin: 0.5rem;
      font-size: 1.8vmin;
      transition: all 0.3s ease;
      text-decoration: none;
      border: 1px solid transparent;
      border-radius: 50px;
      padding: 0.5rem 1.5rem;
      color: #1c6ca2;
      border-color: #8d8d8d;
    }}

    .contact-links .btn:hover {{
      transform: translateY(-3px);
      color: #1c6ca2;
      background-color: #bebebe;
    }}

    .author-hyperref {{
      color: #2180c0;
      text-decoration: none;
    }}

    body.dark-mode .author-hyperref {{
      color: #66b3e7;
    }}

    .right-column {{
      width: 67%;
      overflow-y: auto;
      padding: 10px;
    }}

    .footer {{
      background-color: var(--dark-nav);
      color: white;
      text-align: center;
      position: fixed;
      bottom: 0;
      left: 0;
      width: 100%;
      height: 56px;
      display: flex;
      justify-content: flex-end;
      align-items: center;
      padding-right: 10%;
    }}

    .footer a {{
      color: white;
      margin: 0 10px;
      text-decoration: none;
    }}

    .publication-item {{
      transition: transform 0.3s ease, box-shadow 0.3s ease;
      border: none;
      border-radius: 10px;
      overflow: hidden;
      background-color: #ffffff;
      margin-right: 1rem;
    }}

    .publication-item:hover {{
      transform: translateY(-5px);
      box-shadow: 0 0 15px rgba(0, 0, 0, 0.15);
    }}

    .footer a:hover {{
      color: #ddd;
    }}

    footer .social-icons a {{
      color: white;
      margin-left: 0.5rem;
      font-size: 1rem;
    }}

    @media (max-width: 768px) {{
      .main {{
        flex-direction: column;
        height: auto;
        margin-top: 58px;
      }}

      .left-column,
      .right-column {{
        width: 100%;
        /* Make both columns take full width */
        padding: 1rem;
      }}

      .profile-img {{
        height: auto;
        width: 50%;
        max-width: 200px;
      }}

      .profile-header {{
        font-size: 6vmin;
      }}

      .profile-title {{
        font-size: 3vmin;
      }}

      .publication-img {{
        width: 50%;
        height: auto;
      }}

      .image-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        height: auto;
      }}

      .about-me-header,
      #awards .awards-header,
      #publications .publciations-header,
      #homepage_template .homepage-template-header {{
        font-size: 4vmin;
      }}

      /* Container around awards and publications */
    .award, .publication {{
      display: block;
      width: 100%;
      padding: 0px;
      box-sizing: border-box;
    }}

    /* Fix margin or padding issues */
    .award-item, .publication-item {{
      display: block;
      width: 100%; /* Ensure individual items take full width */
      margin: 0;
      padding: 0px;
    }}

      .about-me {{
        font-size: 2.5vmin;
      }}

      .contact-links a {{
        font-size: 2.5vmin;
        margin: 0.25rem;
        padding: 0.25rem 0.75rem;
      }}

      .footer {{
        position: relative;
        height: auto;
        padding: 1rem;
        justify-content: center;
      }}

      body {{
        overflow-y: auto;
      }}

      .about-me-header::after {{
        top: 5vmin;
      }}
    }}
  </style>
</head>

<body>
  <!-- Navigation Bar -->
  <nav class="navbar navbar-expand-lg fixed-top">
    <div class="container">
      <a class="navbar-brand">{self.name}</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
        aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto align-items-center">
          <li class="nav-item"><a class="nav-link" href="#awards">Awards</a></li>
          <li class="nav-item"><a class="nav-link" href="#publications">Publications</a></li>
          <li class="nav-item"><a class="nav-link" href="#homepage_template">Design</a></li>
          <li class="nav-item">
            <button id="darkModeToggle" class="btn btn-link nav-link" aria-label="Toggle dark mode">
              <i class="fas fa-moon"></i>
            </button>
          </li>
        </ul>
      </div>
    </div>
  </nav>

  <div class="main">
    <div class="left-column" id="container">
      <!-- Profile Image -->
      <img src="assets/profile.jpg" class="profile-img" alt="{self.name}">
      <!-- Scalable Header -->
      <div class="profile-header">{self.name}</div>
      <div class="profile-title">{self.title}</div>
      <div class="contact-links">
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
        <a href="{self.linkedin}" target="_blank"
          class="btn btn-outline-primary">
          <i class="fab fa-linkedin" aria-hidden="true"></i> LinkedIn
        </a>
        <a href="{self.youtube}" target="_blank" class="btn btn-outline-primary">
          <i class="fab fa-youtube" aria-hidden="true"></i> YouTube
        </a>
      </div>
      <div class="about-me-header">About Me</div>
      <div class="about-me">
        <p>{self.bio}</p>
      </div>
    </div>

    <div class="right-column">
      <!-- Awards Section -->
      <section id="awards">
        <h2 class="awards-header">Awards</h2>
        {self.awards}
      </section>

      <!-- Publications Section -->
      <section id="publications">
        <h2 class="publciations-header">Publications</h2>
        {self.publications}
      </section>
      <section id="homepage_template">
        <h2 class="homepage-template-header mb-4">Homepage Template</h2>
        <div class="homepage-template">
          <p>This website's design is inspired by <a href="https://m-niemeyer.github.io/" target="_blank"
              class="author-hyperref">Michael
              Niemeyer's personal site</a>. Checkout his <a href="https://github.com/m-niemeyer/m-niemeyer.github.io"
              target="_blank" class="author-hyperref">GitHub</a>!</p>
        </div>
      </section>
    </div>
  </div>

  <!-- Fixed Footer -->
  <div class="footer">
    <a href="{self.github}" class="text-white" target="_blank"><i class="fab fa-github"></i></a>
    <a href="{self.linkedin}" class="text-white" target="_blank"><i
        class="fab fa-linkedin"></i></a>
  </div>

  <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.2/dist/umd/popper.min.js"></script>
  <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>

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

  function toggleDescription(button) {{
    const description = button.parentElement.nextElementSibling;
    if (description.style.display === 'none' || description.style.display === '') {{
      description.style.display = 'block';
    }} else {{
      description.style.display = 'none';
    }}
  }}

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
</script>

</html>
"""

    def save_website(self):
        website = self._generate_website()

        with open('index.html', 'w') as f:
            f.write(website)

if __name__ == '__main__':
    WebsiteCreator().save_website()