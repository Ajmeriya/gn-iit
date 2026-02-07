"""
Skill Dictionary and Role Mapping for JD Analyzer
Expandable skill list and role keyword mappings
"""

# Comprehensive skill dictionary (case-insensitive matching)
# Organized by category for easy maintenance
SKILLS = [
    # Frontend Technologies
    "React", "React.js", "ReactJS", "Vue", "Vue.js", "Angular", "AngularJS",
    "TypeScript", "JavaScript", "JS", "ES6", "ES7", "ES8",
    "HTML", "HTML5", "CSS", "CSS3", "SASS", "SCSS", "LESS",
    "Bootstrap", "Tailwind CSS", "Material-UI", "Ant Design",
    "Next.js", "Nuxt.js", "Gatsby", "Remix",
    "Webpack", "Vite", "Parcel", "Rollup",
    "Redux", "MobX", "Zustand", "Recoil",
    "Jest", "Cypress", "Selenium", "Playwright",
    
    # Backend Technologies
    "Java", "Spring", "Spring Boot", "Spring MVC", "Spring Security",
    "Python", "Django", "Flask", "FastAPI", "Tornado",
    "Node.js", "Node", "Express", "NestJS", "Koa",
    "C#", ".NET", "ASP.NET", "ASP.NET Core",
    "PHP", "Laravel", "Symfony", "CodeIgniter",
    "Ruby", "Ruby on Rails", "Rails",
    "Go", "Golang", "Rust",
    
    # Databases
    "MySQL", "PostgreSQL", "MongoDB", "Redis", "Cassandra",
    "Oracle", "SQL Server", "SQLite", "DynamoDB",
    "Elasticsearch", "Solr", "Neo4j",
    
    # Cloud & DevOps
    "AWS", "Amazon Web Services", "Azure", "Google Cloud", "GCP",
    "Docker", "Kubernetes", "K8s", "Jenkins", "CI/CD",
    "Git", "GitHub", "GitLab", "Bitbucket",
    "Terraform", "Ansible", "Chef", "Puppet",
    "Linux", "Unix", "Bash", "Shell Scripting",
    
    # Architecture & Patterns
    "Microservices", "REST API", "REST", "GraphQL", "gRPC",
    "SOAP", "WebSocket", "Message Queue", "RabbitMQ", "Kafka",
    "Event-Driven Architecture", "EDA", "Service-Oriented Architecture", "SOA",
    "MVC", "MVP", "MVVM", "Clean Architecture",
    
    # Testing
    "Unit Testing", "Integration Testing", "E2E Testing",
    "JUnit", "TestNG", "PyTest", "Mocha", "Chai",
    "TDD", "BDD", "Test Automation",
    
    # Mobile
    "React Native", "Flutter", "iOS", "Android", "Swift", "Kotlin",
    "Xamarin", "Ionic", "Cordova",
    
    # Data & Analytics
    "Data Science", "Machine Learning", "ML", "Deep Learning",
    "TensorFlow", "PyTorch", "Scikit-learn", "Pandas", "NumPy",
    "Apache Spark", "Hadoop", "Big Data",
    
    # Other Technologies
    "GraphQL", "WebRTC", "OAuth", "JWT", "JWT Token",
    "OAuth2", "OpenID Connect", "SSO",
    "Agile", "Scrum", "Kanban", "DevOps",
    "API Gateway", "Load Balancing", "Caching",
    "Message Broker", "Event Streaming",
]

# Role keyword mapping (order matters - more specific first)
ROLE_MAP = [
    # Full Stack
    (["full stack", "fullstack", "full-stack"], "Full Stack Developer"),
    
    # Frontend
    (["react", "reactjs", "react.js", "vue", "vue.js", "angular", "frontend", "front-end", "ui developer", "ui/ux"], "Frontend Developer"),
    
    # Backend
    (["spring boot", "springboot", "backend", "back-end", "server-side", "api developer"], "Backend Developer"),
    
    # Java-specific
    (["java", "j2ee", "jee"], "Java Developer"),
    
    # Python-specific
    (["python", "django", "flask"], "Python Developer"),
    
    # Node.js-specific
    (["node.js", "nodejs", "node", "express"], "Node.js Developer"),
    
    # .NET-specific
    (["c#", "csharp", ".net", "asp.net", "dotnet"], ".NET Developer"),
    
    # Mobile
    (["mobile", "ios", "android", "react native", "flutter"], "Mobile Developer"),
    
    # DevOps
    (["devops", "sre", "site reliability", "infrastructure", "cloud engineer"], "DevOps Engineer"),
    
    # Data
    (["data scientist", "data engineer", "ml engineer", "machine learning"], "Data Engineer"),
    
    # QA
    (["qa", "quality assurance", "test engineer", "sdet"], "QA Engineer"),
    
    # Default fallback
    ([], "Software Developer"),
]

# Normalization map for skill name standardization
SKILL_NORMALIZATION = {
    "reactjs": "React",
    "react.js": "React",
    "react": "React",
    "vue.js": "Vue",
    "vuejs": "Vue",
    "angularjs": "Angular",
    "js": "JavaScript",
    "javascript": "JavaScript",
    "es6": "JavaScript",
    "es7": "JavaScript",
    "es8": "JavaScript",
    "node": "Node.js",
    "nodejs": "Node.js",
    "springboot": "Spring Boot",
    "spring-boot": "Spring Boot",
    "spring": "Spring Boot",
    "mysql": "MySQL",
    "postgresql": "PostgreSQL",
    "postgres": "PostgreSQL",
    "mongodb": "MongoDB",
    "redis": "Redis",
    "aws": "AWS",
    "amazon web services": "AWS",
    "gcp": "Google Cloud",
    "google cloud": "Google Cloud",
    "azure": "Azure",
    "docker": "Docker",
    "kubernetes": "Kubernetes",
    "k8s": "Kubernetes",
    "rest api": "REST API",
    "rest": "REST API",
    "graphql": "GraphQL",
    "microservices": "Microservices",
    "ci/cd": "CI/CD",
    "cicd": "CI/CD",
    "git": "Git",
    "github": "GitHub",
    "gitlab": "GitLab",
    "jwt": "JWT",
    "oauth": "OAuth",
    "oauth2": "OAuth2",
    "typescript": "TypeScript",
    "ts": "TypeScript",
    "html5": "HTML5",
    "css3": "CSS3",
    "sass": "SASS",
    "scss": "SCSS",
    "less": "LESS",
    "redux": "Redux",
    "jest": "Jest",
    "cypress": "Cypress",
    "selenium": "Selenium",
    "playwright": "Playwright",
    "django": "Django",
    "flask": "Flask",
    "fastapi": "FastAPI",
    "express": "Express",
    "nestjs": "NestJS",
    "laravel": "Laravel",
    "symfony": "Symfony",
    "ruby on rails": "Ruby on Rails",
    "rails": "Ruby on Rails",
    "golang": "Go",
    "go": "Go",
    "rust": "Rust",
    "c#": "C#",
    "csharp": "C#",
    ".net": ".NET",
    "asp.net": "ASP.NET",
    "asp.net core": "ASP.NET Core",
    "dotnet": ".NET",
    "php": "PHP",
    "ruby": "Ruby",
    "python": "Python",
    "java": "Java",
    "react native": "React Native",
    "flutter": "Flutter",
    "ios": "iOS",
    "android": "Android",
    "swift": "Swift",
    "kotlin": "Kotlin",
    "machine learning": "Machine Learning",
    "ml": "Machine Learning",
    "deep learning": "Deep Learning",
    "data science": "Data Science",
    "tensorflow": "TensorFlow",
    "pytorch": "PyTorch",
    "scikit-learn": "Scikit-learn",
    "pandas": "Pandas",
    "numpy": "NumPy",
    "apache spark": "Apache Spark",
    "spark": "Apache Spark",
    "hadoop": "Hadoop",
    "big data": "Big Data",
    "elasticsearch": "Elasticsearch",
    "solr": "Solr",
    "neo4j": "Neo4j",
    "rabbitmq": "RabbitMQ",
    "kafka": "Kafka",
    "terraform": "Terraform",
    "ansible": "Ansible",
    "chef": "Chef",
    "puppet": "Puppet",
    "jenkins": "Jenkins",
    "linux": "Linux",
    "unix": "Unix",
    "bash": "Bash",
    "shell scripting": "Shell Scripting",
    "agile": "Agile",
    "scrum": "Scrum",
    "kanban": "Kanban",
    "devops": "DevOps",
    "tdd": "TDD",
    "bdd": "BDD",
    "test automation": "Test Automation",
    "unit testing": "Unit Testing",
    "integration testing": "Integration Testing",
    "e2e testing": "E2E Testing",
    "junit": "JUnit",
    "testng": "TestNG",
    "pytest": "PyTest",
    "mocha": "Mocha",
    "chai": "Chai",
    "webpack": "Webpack",
    "vite": "Vite",
    "parcel": "Parcel",
    "rollup": "Rollup",
    "next.js": "Next.js",
    "nuxt.js": "Nuxt.js",
    "gatsby": "Gatsby",
    "remix": "Remix",
    "bootstrap": "Bootstrap",
    "tailwind css": "Tailwind CSS",
    "material-ui": "Material-UI",
    "ant design": "Ant Design",
    "mobx": "MobX",
    "zustand": "Zustand",
    "recoil": "Recoil",
    "oracle": "Oracle",
    "sql server": "SQL Server",
    "sqlite": "SQLite",
    "dynamodb": "DynamoDB",
    "cassandra": "Cassandra",
    "websocket": "WebSocket",
    "message queue": "Message Queue",
    "event-driven architecture": "Event-Driven Architecture",
    "eda": "Event-Driven Architecture",
    "service-oriented architecture": "Service-Oriented Architecture",
    "soa": "Service-Oriented Architecture",
    "mvc": "MVC",
    "mvp": "MVP",
    "mvvm": "MVVM",
    "clean architecture": "Clean Architecture",
    "api gateway": "API Gateway",
    "load balancing": "Load Balancing",
    "caching": "Caching",
    "message broker": "Message Broker",
    "event streaming": "Event Streaming",
    "grpc": "gRPC",
    "soap": "SOAP",
    "openid connect": "OpenID Connect",
    "sso": "SSO",
    "webrtc": "WebRTC",
    "xamarin": "Xamarin",
    "ionic": "Ionic",
    "cordova": "Cordova",
    "qa": "QA",
    "quality assurance": "Quality Assurance",
    "test engineer": "Test Engineer",
    "sdet": "SDET",
    "sre": "SRE",
    "site reliability": "Site Reliability",
    "infrastructure": "Infrastructure",
    "cloud engineer": "Cloud Engineer",
    "data scientist": "Data Scientist",
    "data engineer": "Data Engineer",
    "ml engineer": "ML Engineer",
}

