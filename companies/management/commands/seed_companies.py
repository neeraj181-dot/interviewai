from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
from companies.models import Company, InterviewSlot

COMPANIES = [
    {
        'name': 'Google',
        'slug': 'google',
        'logo_icon': 'fab fa-google',
        'color': '#4285f4',
        'description': 'Google LLC is a global technology leader in internet services, AI, cloud computing, and hardware. Known for its rigorous hiring process, innovative culture, and world-class engineering challenges.',
        'hiring_status': 'hiring',
        'difficulty': 'very_hard',
        'salary_min': 180, 'salary_max': 350,
        'open_positions': 42, 'interview_rounds': 5,
        'required_skills': 'Python,Algorithms,System Design,Data Structures,Problem Solving,LeetCode,Distributed Systems',
        'hiring_deadline': date.today() + timedelta(days=45),
        'website': 'https://careers.google.com',
        'careers_url': 'https://careers.google.com',
        'culture_tags': 'Innovation,Open Culture,20% Projects,Data-Driven,Moonshots',
        'ai_tips': 'Google focuses heavily on Data Structures & Algorithms — practice LeetCode Hard daily.|System Design is critical: study distributed systems, scalability, and Google-scale architecture.|Behavioral questions follow the STAR method — prepare 5-6 strong stories.|Googleyness matters: show curiosity, collaboration, and comfort with ambiguity.|Practice coding on a whiteboard or Google Docs without autocomplete.|Study Google products deeply — interviewers love candidates who understand their ecosystem.',
        'interview_process': 'Online Coding Assessment (90 min, 2-3 LeetCode problems)|Technical Phone Screen (45 min, DSA focus)|Onsite Round 1: Algorithms & Data Structures|Onsite Round 2: System Design (design YouTube, Google Maps)|Onsite Round 3: Behavioral + Googleyness|Hiring Committee Review',
        'is_featured': True, 'order': 1,
    },
    {
        'name': 'Microsoft',
        'slug': 'microsoft',
        'logo_icon': 'fab fa-microsoft',
        'color': '#00a4ef',
        'description': 'Microsoft Corporation builds software, cloud services (Azure), and hardware. A top employer for engineers worldwide with strong emphasis on growth mindset and collaborative culture.',
        'hiring_status': 'hiring',
        'difficulty': 'hard',
        'salary_min': 160, 'salary_max': 300,
        'open_positions': 67, 'interview_rounds': 4,
        'required_skills': 'C#,.NET,Azure,Python,System Design,SQL,Problem Solving,OOP',
        'hiring_deadline': date.today() + timedelta(days=60),
        'website': 'https://careers.microsoft.com',
        'careers_url': 'https://careers.microsoft.com',
        'culture_tags': 'Growth Mindset,Inclusive,Azure,Cloud-First,Diversity',
        'ai_tips': 'Microsoft values Growth Mindset — show how you learn from failures and adapt.|Azure knowledge is a big plus: understand cloud fundamentals, microservices, and DevOps.|Coding interviews focus on OOP, design patterns, and clean code — not just raw algorithms.|Behavioral questions often ask about collaboration and handling disagreements professionally.|Study the Microsoft Leadership Principles and connect your answers to them.|Practice system design with Azure services: App Service, Cosmos DB, Service Bus.',
        'interview_process': 'Online Assessment (coding + logical reasoning)|Technical Screen with Hiring Manager|Onsite Loop Round 1: Coding & Problem Solving|Onsite Loop Round 2: System Design|Onsite Loop Round 3: Behavioral + Culture Fit|As-Appropriate Interview (senior review)',
        'is_featured': True, 'order': 2,
    },
    {
        'name': 'Amazon',
        'slug': 'amazon',
        'logo_icon': 'fab fa-amazon',
        'color': '#ff9900',
        'description': 'Amazon is the world\'s largest e-commerce and cloud platform (AWS). Every interview is deeply tied to Amazon\'s 16 Leadership Principles — you must know them cold.',
        'hiring_status': 'hiring',
        'difficulty': 'hard',
        'salary_min': 150, 'salary_max': 280,
        'open_positions': 89, 'interview_rounds': 5,
        'required_skills': 'Java,Python,AWS,System Design,Leadership Principles,Distributed Systems,SQL',
        'hiring_deadline': date.today() + timedelta(days=30),
        'website': 'https://www.amazon.jobs',
        'careers_url': 'https://www.amazon.jobs',
        'culture_tags': 'Leadership Principles,Customer Obsession,Ownership,Frugality,Bias for Action',
        'ai_tips': 'Amazon Leadership Principles are non-negotiable — memorize all 16 and prepare STAR stories for each.|Every behavioral question maps to a Leadership Principle: Customer Obsession, Ownership, Invent & Simplify.|Coding rounds focus on Java or Python — practice medium/hard LeetCode problems.|System design at Amazon scale: think about high availability, fault tolerance, and cost efficiency.|The Bar Raiser is a senior interviewer who ensures you raise the bar — impress them.|Prepare for the "Why Amazon?" question with specific LP-aligned examples.',
        'interview_process': 'Online Assessment (2 coding problems + work simulation)|Phone Screen with Hiring Manager (LP + coding)|Virtual Onsite Round 1: Coding (DSA)|Virtual Onsite Round 2: System Design (design Amazon cart, Prime Video)|Virtual Onsite Round 3: Leadership Principles deep dive|Bar Raiser Round (cross-team senior interviewer)',
        'is_featured': True, 'order': 3,
    },
    {
        'name': 'Meta',
        'slug': 'meta',
        'logo_icon': 'fas fa-infinity',
        'color': '#0668e1',
        'description': 'Meta Platforms builds Facebook, Instagram, WhatsApp, and the Metaverse. Strong focus on impact, speed, and cutting-edge AI/AR/VR engineering at massive scale.',
        'hiring_status': 'limited',
        'difficulty': 'very_hard',
        'salary_min': 170, 'salary_max': 320,
        'open_positions': 18, 'interview_rounds': 5,
        'required_skills': 'Python,C++,System Design,Algorithms,React,Distributed Systems,ML',
        'hiring_deadline': date.today() + timedelta(days=20),
        'website': 'https://www.metacareers.com',
        'careers_url': 'https://www.metacareers.com',
        'culture_tags': 'Move Fast,Impact,Openness,Bold Bets,Metaverse,AI-First',
        'ai_tips': 'Meta interviews are among the hardest — expect LeetCode Hard problems in coding rounds.|System design focuses on social graph scale: news feed, messaging, real-time systems.|Meta values "Move Fast" — show you can ship quickly and iterate based on data.|Behavioral questions focus on impact and ownership: quantify your achievements.|Study React deeply if applying for frontend roles — Meta created it.|AI/ML knowledge is increasingly valued across all engineering roles at Meta.',
        'interview_process': 'Recruiter Screen (background + motivation)|Technical Phone Screen (45 min coding)|Onsite Round 1: Coding (2 problems, 45 min each)|Onsite Round 2: System Design (design Instagram feed, WhatsApp)|Onsite Round 3: Behavioral (impact, collaboration, growth)|Hiring Committee + Compensation Discussion',
        'is_featured': True, 'order': 4,
    },
    {
        'name': 'TCS',
        'slug': 'tcs',
        'logo_icon': 'fas fa-building',
        'color': '#00d4ff',
        'description': 'Tata Consultancy Services is India\'s largest IT company with 600,000+ employees globally. Excellent entry-level opportunities with structured training programs (TCS iON, TCS NQT).',
        'hiring_status': 'hiring',
        'difficulty': 'medium',
        'salary_min': 35, 'salary_max': 80,
        'open_positions': 250, 'interview_rounds': 3,
        'required_skills': 'Java,Python,SQL,Communication,Aptitude,Problem Solving,DBMS',
        'hiring_deadline': date.today() + timedelta(days=90),
        'website': 'https://www.tcs.com/careers',
        'careers_url': 'https://www.tcs.com/careers',
        'culture_tags': 'Learning,Stability,Global Projects,Training,Work-Life Balance',
        'ai_tips': 'TCS NQT (National Qualifier Test) is the entry point — practice aptitude, verbal, and coding sections.|Focus on core CS fundamentals: DBMS, OS, Networks, and OOP concepts.|Communication skills are heavily evaluated — practice speaking clearly and confidently.|TCS values loyalty and learning — show enthusiasm for long-term growth.|Java and Python are the primary languages — be comfortable with basic programs.|The HR round is crucial at TCS — prepare your "tell me about yourself" thoroughly.',
        'interview_process': 'TCS NQT Online Test (Aptitude + Verbal + Coding)|Technical Interview Round 1 (CS fundamentals, coding)|Managerial Round (project discussion, problem-solving)|HR Round (communication, culture fit, salary negotiation)',
        'is_featured': False, 'order': 5,
    },
    {
        'name': 'Infosys',
        'slug': 'infosys',
        'logo_icon': 'fas fa-building',
        'color': '#007cc3',
        'description': 'Infosys is a global leader in digital services and consulting with 300,000+ employees. Known for InfyTQ platform, strong fresher programs, and excellent training at Mysore campus.',
        'hiring_status': 'hiring',
        'difficulty': 'medium',
        'salary_min': 32, 'salary_max': 75,
        'open_positions': 180, 'interview_rounds': 3,
        'required_skills': 'Java,Python,SQL,Aptitude,Communication,Logical Reasoning,OOP',
        'hiring_deadline': date.today() + timedelta(days=75),
        'website': 'https://www.infosys.com/careers',
        'careers_url': 'https://www.infosys.com/careers',
        'culture_tags': 'Learning,Ethics,Diversity,Innovation,Client-Focus',
        'ai_tips': 'Infosys InfyTQ certification significantly boosts your chances — complete it before applying.|The Infosys Aptitude test covers quantitative, logical, and verbal reasoning — practice daily.|Java is the primary language at Infosys — be comfortable with OOP, collections, and basic programs.|Infosys values ethical behavior and client focus — align your answers to these values.|The HR round focuses on adaptability and willingness to relocate — be prepared.|Study basic SQL queries, joins, and normalization for the technical round.',
        'interview_process': 'InfyTQ Online Assessment (Aptitude + Coding)|Technical Interview (Java/Python, SQL, OOP concepts)|HR Interview (communication, adaptability, career goals)',
        'is_featured': False, 'order': 6,
    },
    {
        'name': 'Wipro',
        'slug': 'wipro',
        'logo_icon': 'fas fa-building',
        'color': '#9b59b6',
        'description': 'Wipro Limited is a leading global IT and consulting company focused on digital transformation. Known for WILP (Work Integrated Learning Program) and strong cloud/AI practices.',
        'hiring_status': 'hiring',
        'difficulty': 'medium',
        'salary_min': 30, 'salary_max': 70,
        'open_positions': 200, 'interview_rounds': 3,
        'required_skills': 'Java,Python,SQL,Communication,Aptitude,DBMS,Cloud Basics',
        'hiring_deadline': date.today() + timedelta(days=80),
        'website': 'https://careers.wipro.com',
        'careers_url': 'https://careers.wipro.com',
        'culture_tags': 'Sustainability,Inclusion,Digital,Cloud,Agile',
        'ai_tips': 'Wipro NLTH (National Level Talent Hunt) is the main entry test — practice all sections.|Focus on aptitude: quantitative reasoning, logical puzzles, and verbal ability.|Wipro values cloud and digital skills — basic AWS/Azure knowledge is a plus.|The technical round covers Java/Python basics, SQL, and DBMS fundamentals.|Show enthusiasm for Wipro\'s sustainability and digital transformation mission.|Communication and presentation skills are key differentiators in the HR round.',
        'interview_process': 'Wipro NLTH Online Test (Aptitude + Essay + Coding)|Technical Interview Round (programming, DBMS, OS)|HR Interview (communication, goals, culture fit)',
        'is_featured': False, 'order': 7,
    },
    {
        'name': 'Startup Hub',
        'slug': 'startup-hub',
        'logo_icon': 'fas fa-rocket',
        'color': '#ff6b9d',
        'description': 'A curated network of high-growth startups seeking talented engineers. Fast-paced environment, equity compensation, direct product impact, and rapid career growth.',
        'hiring_status': 'upcoming',
        'difficulty': 'medium',
        'salary_min': 80, 'salary_max': 160,
        'open_positions': 35, 'interview_rounds': 3,
        'required_skills': 'React,Node.js,Python,Django,PostgreSQL,AWS,Startup Mindset,Full Stack',
        'hiring_deadline': date.today() + timedelta(days=15),
        'website': 'https://www.ycombinator.com/jobs',
        'careers_url': 'https://www.ycombinator.com/jobs',
        'culture_tags': 'Move Fast,Equity,Impact,Ownership,Remote-Friendly,Agile',
        'ai_tips': 'Startups value full-stack versatility — be comfortable across frontend, backend, and DevOps.|Show ownership mentality: describe projects where you drove end-to-end delivery.|Startup interviews are often more conversational — focus on problem-solving approach.|Equity and growth potential matter more than base salary — understand vesting schedules.|Demonstrate passion for the product domain — research the startup thoroughly before interviews.|Side projects and open-source contributions are highly valued over academic credentials.',
        'interview_process': 'Founder/CTO Screen (culture fit, motivation, background)|Take-Home Project (build a small feature in 48 hours)|Technical Deep Dive (code review + architecture discussion)',
        'is_featured': False, 'order': 8,
    },
]

SLOT_ROUNDS = ['online_test', 'technical_1', 'technical_2', 'hr']


class Command(BaseCommand):
    help = 'Seed companies with rich AI data and interview slots'

    def add_arguments(self, parser):
        parser.add_argument('--flush', action='store_true')

    def handle(self, *args, **options):
        if options['flush']:
            InterviewSlot.objects.all().delete()
            Company.objects.all().delete()
            self.stdout.write('Flushed company data.')

        self.stdout.write(self.style.WARNING('Seeding companies...'))

        for c_data in COMPANIES:
            company, created = Company.objects.get_or_create(
                slug=c_data['slug'], defaults=c_data
            )
            if not created:
                for k, v in c_data.items():
                    setattr(company, k, v)
                company.save()
            self.stdout.write(f'  {"+" if created else "~"} {company.name} ({company.careers_url})')

            if company.hiring_status in ('hiring', 'limited'):
                rounds = SLOT_ROUNDS[:min(company.interview_rounds, 4)]
                for i, round_type in enumerate(rounds):
                    slot_date = date.today() + timedelta(days=7 + i * 7)
                    slot, s_created = InterviewSlot.objects.get_or_create(
                        company=company, round_type=round_type, date=slot_date,
                        defaults={
                            'time_start': f'{9 + i * 2}:00',
                            'time_end': f'{10 + i * 2}:00',
                            'max_candidates': 5 if company.hiring_status == 'hiring' else 2,
                            'status': 'available',
                        }
                    )
                    if s_created:
                        self.stdout.write(f'    + Slot: {round_type} on {slot_date}')

        self.stdout.write(self.style.SUCCESS(
            f'\nDone! Companies: {Company.objects.count()}, Slots: {InterviewSlot.objects.count()}'
        ))
