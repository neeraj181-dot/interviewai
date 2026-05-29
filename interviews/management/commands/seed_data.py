from django.core.management.base import BaseCommand
from interviews.models import Category, Question


CATEGORIES = [
    {'name': 'Python', 'slug': 'python', 'description': 'Master Python from basics to advanced concepts', 'icon': 'fab fa-python', 'color': '#00d4ff'},
    {'name': 'Django', 'slug': 'django', 'description': 'Django web framework — ORM, views, APIs and more', 'icon': 'fas fa-server', 'color': '#00ff88'},
    {'name': 'HR Interview', 'slug': 'hr', 'description': 'Behavioral, situational and soft-skills questions', 'icon': 'fas fa-users', 'color': '#ff6b9d'},
    {'name': 'Web Development', 'slug': 'web', 'description': 'HTML, CSS, JavaScript, REST APIs and browser concepts', 'icon': 'fas fa-globe', 'color': '#ffd700'},
]

QUESTIONS = {
    'python': {
        'easy': [
            ('What is Python and what are its key features?', 'interpreted,dynamic,readable,versatile,open-source,high-level', 'Python is a high-level, interpreted, dynamically typed language known for readability and versatility.', 8),
            ('What is the difference between a list and a tuple?', 'mutable,immutable,list,tuple,changeable,ordered', 'Lists are mutable (can be changed); tuples are immutable (cannot be changed after creation).', 8),
            ('What are Python list comprehensions?', 'list,comprehension,concise,loop,expression,brackets', 'List comprehensions provide a concise way to create lists: [x*2 for x in range(10)].', 8),
            ('Explain Python\'s *args and **kwargs.', 'args,kwargs,variable,arguments,positional,keyword', '*args collects extra positional arguments; **kwargs collects extra keyword arguments.', 8),
            ('What is the difference between == and is in Python?', 'equality,identity,value,object,reference,is,==', '== checks value equality; is checks object identity (same memory address).', 8),
            ('What are Python\'s built-in data types?', 'int,float,str,list,tuple,dict,set,bool,bytes', 'Python built-ins include int, float, str, list, tuple, dict, set, bool, bytes, and NoneType.', 8),
            ('How do you handle exceptions in Python?', 'try,except,finally,raise,exception,error,handling', 'Use try/except blocks to catch exceptions, finally for cleanup, and raise to throw exceptions.', 8),
            ('What is a Python module and how do you import it?', 'module,import,from,package,namespace,file', 'A module is a .py file containing code. Import with import module or from module import name.', 8),
            ('What is the difference between range() and xrange()?', 'range,xrange,Python 3,list,iterator,memory', 'In Python 3, range() returns an iterator (like Python 2\'s xrange). xrange() no longer exists.', 8),
            ('What is a Python dictionary and how do you use it?', 'dictionary,dict,key,value,mapping,hash,lookup', 'A dict is a mutable key-value mapping. Access values with dict[key] or dict.get(key).', 8),
        ],
        'medium': [
            ('What is a Python decorator and how does it work?', 'decorator,function,wrapper,@,higher-order,closure', 'A decorator wraps a function to extend its behavior using the @ syntax and closures.', 10),
            ('What is a Python generator and what is yield used for?', 'generator,yield,iterator,lazy,memory,next', 'Generators use yield to produce values lazily, saving memory compared to returning a full list.', 10),
            ('What is the difference between __str__ and __repr__?', 'str,repr,string,representation,readable,developer,dunder', '__str__ is for human-readable output; __repr__ is for unambiguous developer/debug representation.', 10),
            ('What is the difference between deep copy and shallow copy?', 'deep,shallow,copy,reference,nested,independent,module', 'Shallow copy references nested objects; deep copy creates fully independent copies recursively.', 10),
            ('Explain Python\'s context managers and the with statement.', 'context,manager,with,__enter__,__exit__,resource,cleanup', 'Context managers handle setup/teardown via __enter__/__exit__, used with the with statement.', 10),
            ('What are Python\'s magic/dunder methods?', 'dunder,magic,__init__,__str__,__len__,special,method', 'Dunder methods like __init__, __str__, __len__ define object behavior for built-in operations.', 10),
            ('What is the difference between a class method and a static method?', 'classmethod,staticmethod,cls,self,decorator,instance', '@classmethod receives cls; @staticmethod receives no implicit first argument.', 10),
            ('How does Python\'s garbage collection work?', 'garbage,collection,reference,counting,cyclic,gc,memory', 'Python uses reference counting plus a cyclic garbage collector for circular references.', 10),
            ('What is a lambda function in Python?', 'lambda,anonymous,function,expression,inline,one-line', 'A lambda is an anonymous single-expression function: lambda x: x*2.', 10),
            ('Explain Python\'s map(), filter(), and reduce() functions.', 'map,filter,reduce,functional,iterable,higher-order', 'map applies a function to each item; filter selects items; reduce folds items into one value.', 10),
        ],
        'hard': [
            ('Explain Python\'s GIL (Global Interpreter Lock).', 'GIL,thread,mutex,CPython,concurrency,lock,bytecode', 'The GIL is a CPython mutex allowing only one thread to execute bytecode at a time.', 15),
            ('What are Python metaclasses and when would you use them?', 'metaclass,type,class,creation,__new__,__init__,customize', 'Metaclasses are classes of classes, controlling class creation via __new__ and __init__.', 15),
            ('Explain Python\'s descriptor protocol.', 'descriptor,__get__,__set__,__delete__,property,attribute', 'Descriptors define __get__, __set__, __delete__ to customize attribute access on classes.', 15),
            ('What is the difference between multiprocessing and multithreading in Python?', 'multiprocessing,multithreading,GIL,process,thread,parallel,CPU', 'Multiprocessing bypasses the GIL with separate processes; threading shares memory but is GIL-limited.', 15),
            ('Explain Python\'s asyncio and async/await.', 'asyncio,async,await,coroutine,event loop,non-blocking,concurrent', 'asyncio enables concurrent I/O via coroutines, async/await syntax, and an event loop.', 15),
            ('What are Python slots and when should you use them?', '__slots__,memory,attribute,dict,optimization,class', '__slots__ replaces __dict__ on instances, reducing memory usage for classes with fixed attributes.', 15),
            ('Explain the MRO (Method Resolution Order) in Python.', 'MRO,C3,linearization,multiple inheritance,super,resolution,order', 'MRO uses C3 linearization to determine method lookup order in multiple inheritance hierarchies.', 15),
            ('What is a Python abstract base class (ABC)?', 'ABC,abstract,base,class,interface,abstractmethod,enforce', 'ABCs define interfaces using @abstractmethod, enforcing subclasses to implement required methods.', 15),
            ('How does Python\'s import system work internally?', 'import,sys.modules,finder,loader,__init__,package,cache', 'Python checks sys.modules cache, then uses finders/loaders to locate and execute module code.', 15),
            ('What are Python\'s weak references and when are they useful?', 'weakref,weak,reference,garbage,collection,cache,circular', 'Weak references don\'t prevent garbage collection, useful for caches and avoiding circular references.', 15),
        ],
    },
    'django': {
        'easy': [
            ('What is Django and what is it used for?', 'web,framework,Python,MTV,batteries,rapid,development', 'Django is a high-level Python web framework for rapid development with a batteries-included philosophy.', 8),
            ('Explain Django\'s MVT architecture.', 'model,view,template,MVT,architecture,pattern,separation', 'MVT: Model handles data, View handles logic, Template handles presentation.', 8),
            ('What is Django ORM and what are its advantages?', 'ORM,object,relational,mapping,database,model,query,SQL', 'Django ORM maps Python classes to database tables, enabling database operations without raw SQL.', 8),
            ('What is a Django migration and why is it important?', 'migration,schema,database,makemigrations,migrate,version,sync', 'Migrations propagate model changes to the database schema, keeping them in sync.', 8),
            ('Explain Django\'s authentication system.', 'authentication,user,login,logout,session,permission,auth,built-in', 'Django provides a built-in auth system with User model, login/logout views, and permissions.', 8),
            ('What is a Django URL pattern?', 'URL,pattern,path,urlpatterns,routing,view,name', 'URL patterns map URL paths to view functions using path() or re_path() in urlpatterns.', 8),
            ('What is a Django template and how does it work?', 'template,HTML,tag,filter,context,render,variable', 'Templates are HTML files with Django template language tags ({% %}) and variables ({{ }}).', 8),
            ('What is the Django admin interface?', 'admin,interface,CRUD,register,ModelAdmin,superuser,built-in', 'Django admin is a built-in CRUD interface for managing models, accessible to superusers.', 8),
            ('What is a Django model?', 'model,class,field,database,table,ORM,CharField,IntegerField', 'A Django model is a Python class that maps to a database table, with fields as class attributes.', 8),
            ('How do you create a superuser in Django?', 'superuser,createsuperuser,manage.py,admin,username,password', 'Run python manage.py createsuperuser and follow the prompts to create an admin user.', 8),
        ],
        'medium': [
            ('What is Django middleware and how does it work?', 'middleware,request,response,process,hook,pipeline,MIDDLEWARE', 'Middleware hooks into Django\'s request/response pipeline to process requests globally.', 10),
            ('How does Django handle CSRF protection?', 'CSRF,token,middleware,form,cross-site,request,forgery,{% csrf_token %}', 'Django uses CSRF tokens in forms and CsrfViewMiddleware to prevent cross-site request forgery.', 10),
            ('What are Django signals and when would you use them?', 'signal,sender,receiver,post_save,pre_save,dispatch,decouple,connect', 'Signals allow decoupled apps to react to events like post_save or pre_delete.', 10),
            ('What is the difference between ForeignKey, OneToOneField, and ManyToManyField?', 'ForeignKey,OneToOne,ManyToMany,relationship,database,field', 'ForeignKey is many-to-one; OneToOneField is one-to-one; ManyToManyField is many-to-many.', 10),
            ('What are Django class-based views (CBVs)?', 'CBV,class,view,ListView,DetailView,CreateView,generic,mixin', 'CBVs use Python classes with mixins for reusable view logic, like ListView and DetailView.', 10),
            ('What is Django REST Framework (DRF)?', 'DRF,REST,API,serializer,ViewSet,router,authentication,permission', 'DRF is a toolkit for building Web APIs with serializers, ViewSets, and authentication.', 10),
            ('How do you optimize Django database queries?', 'select_related,prefetch_related,query,N+1,optimization,index,only', 'Use select_related for FK joins, prefetch_related for M2M, and avoid N+1 query problems.', 10),
            ('What is Django\'s caching framework?', 'cache,memcached,redis,cache_page,per-view,low-level,backend', 'Django supports per-site, per-view, and low-level caching with backends like Redis or Memcached.', 10),
            ('What are Django form classes and how do they work?', 'form,Form,ModelForm,validation,clean,widget,field', 'Django forms handle HTML form rendering, data validation, and cleaning via Form/ModelForm classes.', 10),
            ('What is Django\'s settings.py and what are key settings?', 'settings,DEBUG,DATABASES,INSTALLED_APPS,MIDDLEWARE,SECRET_KEY,STATIC', 'settings.py configures the project: DEBUG, DATABASES, INSTALLED_APPS, MIDDLEWARE, SECRET_KEY, etc.', 10),
        ],
        'hard': [
            ('What is the difference between select_related and prefetch_related?', 'select_related,prefetch_related,JOIN,foreign key,many-to-many,query,SQL', 'select_related uses SQL JOIN for FK/O2O; prefetch_related does separate queries for M2M.', 15),
            ('How does Django\'s ORM generate SQL queries?', 'QuerySet,lazy,SQL,compiler,backend,evaluate,chain', 'QuerySets are lazy; SQL is generated when evaluated. Django uses a query compiler per database backend.', 15),
            ('Explain Django\'s content types framework.', 'ContentType,GenericForeignKey,generic,relation,polymorphic,app,model', 'ContentTypes enable generic relations to any model using GenericForeignKey and ContentType model.', 15),
            ('What are Django custom management commands?', 'management,command,BaseCommand,handle,add_arguments,manage.py', 'Custom commands extend BaseCommand, implement handle(), and are placed in management/commands/.', 15),
            ('How do you implement custom authentication backends in Django?', 'authentication,backend,authenticate,get_user,AUTHENTICATION_BACKENDS,custom', 'Custom backends implement authenticate() and get_user(), registered in AUTHENTICATION_BACKENDS.', 15),
            ('What is Django\'s transaction management?', 'transaction,atomic,savepoint,rollback,commit,database,ACID', 'Django uses atomic() for transactions, ensuring ACID compliance with savepoints and rollbacks.', 15),
            ('How do you implement Django channels for WebSockets?', 'channels,WebSocket,ASGI,consumer,layer,async,real-time', 'Django Channels extends Django with ASGI, enabling WebSocket consumers and async messaging.', 15),
            ('What are Django\'s database routers?', 'router,database,multi-db,db_for_read,db_for_write,allow_migrate', 'Database routers control which database is used for reads, writes, and migrations in multi-DB setups.', 15),
            ('Explain Django\'s permission system in detail.', 'permission,group,has_perm,codename,object-level,guardian,model', 'Django permissions are model-level (add/change/delete/view) and can be extended to object-level.', 15),
            ('How do you deploy a Django application to production?', 'gunicorn,nginx,WSGI,ALLOWED_HOSTS,DEBUG,collectstatic,environment', 'Use gunicorn/uWSGI + nginx, set DEBUG=False, configure ALLOWED_HOSTS, and run collectstatic.', 15),
        ],
    },
    'hr': {
        'easy': [
            ('Tell me about yourself and your professional background.', 'experience,skills,background,professional,career,education,summary', 'Cover education, relevant experience, key skills, and career goals concisely.', 8),
            ('What are your greatest strengths?', 'strength,skill,quality,asset,relevant,example,demonstrate', 'Mention 2-3 genuine strengths relevant to the role with brief examples.', 8),
            ('Why do you want to work for our company?', 'company,culture,mission,values,opportunity,growth,research,align', 'Research the company and align your answer with their mission, culture, and the role.', 8),
            ('Where do you see yourself in 5 years?', 'goal,growth,career,future,develop,leadership,skill,ambition', 'Show ambition aligned with the company\'s growth opportunities and your development.', 8),
            ('What motivates you in your work?', 'motivate,passion,challenge,learn,achieve,impact,growth,drive', 'Be authentic — mention intrinsic motivators like learning, impact, and problem-solving.', 8),
            ('How would your colleagues describe you?', 'colleague,team,describe,quality,reliable,collaborative,feedback', 'Mention positive traits backed by examples: reliable, collaborative, detail-oriented.', 8),
            ('What is your greatest weakness?', 'weakness,improve,honest,growth,learning,working,overcome', 'Mention a real weakness you are actively working to improve, showing self-awareness.', 8),
            ('Why are you leaving your current job?', 'leaving,reason,growth,opportunity,challenge,positive,forward', 'Stay positive — focus on growth opportunities rather than negatives about current employer.', 8),
            ('What are your salary expectations?', 'salary,expectation,research,market,range,negotiate,value', 'Research market rates, give a range based on your skills and experience.', 8),
            ('Do you have any questions for us?', 'question,culture,team,role,growth,opportunity,curious,engage', 'Always ask thoughtful questions about the role, team culture, or growth opportunities.', 8),
        ],
        'medium': [
            ('Describe a challenging situation you faced and how you resolved it.', 'challenge,situation,action,result,STAR,problem,solution,overcome', 'Use the STAR method: Situation, Task, Action, Result to structure your answer.', 10),
            ('How do you handle working under pressure and tight deadlines?', 'pressure,deadline,prioritize,manage,calm,organize,time,strategy', 'Describe time management strategies, prioritization, and give a real example.', 10),
            ('Describe your experience working in a team environment.', 'team,collaborate,communicate,contribute,role,cooperation,conflict', 'Highlight collaboration, communication, conflict resolution, and your contributions.', 10),
            ('Tell me about a time you failed and what you learned.', 'failure,learn,mistake,recover,lesson,growth,resilience,improve', 'Be honest about a real failure, focus on what you learned and how you improved.', 10),
            ('How do you prioritize tasks when you have multiple deadlines?', 'prioritize,deadline,urgent,important,matrix,organize,manage,focus', 'Describe your prioritization framework (e.g., Eisenhower matrix) with a real example.', 10),
            ('Tell me about a time you showed leadership.', 'leadership,initiative,team,guide,decision,responsibility,outcome', 'Describe a situation where you took initiative, guided others, and achieved results.', 10),
            ('How do you handle conflict with a coworker?', 'conflict,resolve,communicate,listen,empathy,professional,solution', 'Describe a calm, professional approach: listen, communicate openly, find common ground.', 10),
            ('What is your approach to learning new technologies?', 'learn,technology,adapt,course,practice,documentation,experiment', 'Describe your learning process: documentation, courses, hands-on practice, and community.', 10),
            ('Tell me about a time you went above and beyond.', 'above,beyond,extra,initiative,impact,result,dedication,effort', 'Share a specific example where you exceeded expectations and the positive outcome.', 10),
            ('How do you give and receive feedback?', 'feedback,constructive,listen,improve,specific,actionable,growth', 'Describe giving specific, actionable feedback and receiving it with openness to grow.', 10),
        ],
        'hard': [
            ('Describe a time you had to make a difficult decision with incomplete information.', 'decision,incomplete,risk,analyze,judgment,outcome,ambiguity,data', 'Describe your decision-making process under uncertainty, the risks you weighed, and the outcome.', 15),
            ('How have you managed a project from start to finish?', 'project,manage,plan,execute,stakeholder,timeline,budget,deliver', 'Walk through planning, stakeholder management, execution, and delivery with a real example.', 15),
            ('Tell me about a time you influenced someone without authority.', 'influence,persuade,authority,stakeholder,communication,trust,outcome', 'Describe how you built trust, communicated value, and persuaded without formal authority.', 15),
            ('How do you handle a situation where you disagree with your manager?', 'disagree,manager,professional,communicate,respect,data,outcome', 'Describe respectfully presenting your perspective with data, then accepting the final decision.', 15),
            ('Describe a time you drove significant change in an organization.', 'change,drive,initiative,resistance,stakeholder,impact,transformation', 'Describe identifying the need, building buy-in, overcoming resistance, and measuring impact.', 15),
            ('How do you build relationships with difficult stakeholders?', 'stakeholder,relationship,difficult,empathy,trust,communication,align', 'Describe understanding their perspective, finding common ground, and building trust over time.', 15),
            ('Tell me about a time you had to deliver bad news.', 'bad news,deliver,honest,empathy,solution,professional,communicate', 'Describe being direct, empathetic, and solution-focused when delivering difficult information.', 15),
            ('How do you stay current with industry trends?', 'industry,trend,learn,conference,publication,network,adapt,current', 'Describe reading publications, attending conferences, networking, and applying new knowledge.', 15),
            ('Describe your approach to mentoring junior team members.', 'mentor,junior,guide,teach,patience,growth,feedback,support', 'Describe understanding their goals, providing guidance, giving feedback, and celebrating growth.', 15),
            ('How do you measure your own success?', 'success,measure,goal,KPI,impact,growth,reflection,outcome', 'Describe setting clear goals, tracking KPIs, reflecting on impact, and continuous improvement.', 15),
        ],
    },
    'web': {
        'easy': [
            ('What is the difference between HTML, CSS, and JavaScript?', 'HTML,structure,CSS,style,JavaScript,behavior,content,presentation', 'HTML provides structure, CSS handles styling, JavaScript adds interactivity.', 8),
            ('Explain the CSS Box Model.', 'box model,margin,border,padding,content,width,height,layout', 'The box model consists of content, padding, border, and margin layers around every element.', 8),
            ('What is the difference between GET and POST HTTP methods?', 'GET,POST,request,data,URL,body,idempotent,secure', 'GET retrieves data via URL params; POST sends data in the request body.', 8),
            ('What is the difference between localStorage and sessionStorage?', 'localStorage,sessionStorage,persist,session,browser,storage,expire,tab', 'localStorage persists until cleared; sessionStorage clears when the tab is closed.', 8),
            ('What is responsive web design?', 'responsive,media query,flexible,viewport,mobile,breakpoint,fluid,adapt', 'Responsive design adapts layouts to different screen sizes using media queries and fluid grids.', 8),
            ('What is the DOM?', 'DOM,document,object,model,tree,node,element,JavaScript', 'The DOM is a tree representation of an HTML document that JavaScript can manipulate.', 8),
            ('What is the difference between inline, block, and inline-block elements?', 'inline,block,inline-block,display,flow,width,height,layout', 'Block takes full width; inline flows with text; inline-block is inline but accepts width/height.', 8),
            ('What is a CSS selector?', 'selector,class,id,element,attribute,pseudo,specificity,target', 'CSS selectors target HTML elements: by tag, class (.), id (#), attribute, or pseudo-class.', 8),
            ('What is an HTML semantic element?', 'semantic,HTML5,header,footer,article,section,nav,meaning', 'Semantic elements like header, footer, article, section convey meaning to browsers and screen readers.', 8),
            ('What is the difference between HTTP and HTTPS?', 'HTTP,HTTPS,SSL,TLS,secure,encrypted,certificate,protocol', 'HTTPS encrypts data with SSL/TLS, providing security over plain HTTP.', 8),
        ],
        'medium': [
            ('Explain CSS Flexbox and its main properties.', 'flexbox,flex,justify-content,align-items,flex-direction,container,item,wrap', 'Flexbox distributes space and aligns items in a container using flex properties.', 10),
            ('What is REST API and what are its principles?', 'REST,stateless,resource,HTTP,endpoint,CRUD,uniform,interface', 'REST uses HTTP methods, stateless communication, and resource-based URLs.', 10),
            ('What is the difference between synchronous and asynchronous JavaScript?', 'sync,async,blocking,non-blocking,callback,promise,await,event loop', 'Sync code blocks execution; async code (callbacks, promises, async/await) is non-blocking.', 10),
            ('What is CSS Grid and how does it differ from Flexbox?', 'grid,CSS,two-dimensional,row,column,flexbox,one-dimensional,layout', 'CSS Grid is 2D (rows and columns); Flexbox is 1D (row or column). Use Grid for page layout.', 10),
            ('What is a JavaScript Promise?', 'promise,async,resolve,reject,then,catch,pending,fulfilled', 'A Promise represents an async operation with states: pending, fulfilled, or rejected.', 10),
            ('What is CORS and why does it matter?', 'CORS,cross-origin,resource,sharing,header,browser,security,policy', 'CORS controls cross-origin requests via HTTP headers, preventing unauthorized resource access.', 10),
            ('What is the difference between cookies, localStorage, and sessionStorage?', 'cookie,localStorage,sessionStorage,storage,expire,server,client,size', 'Cookies are sent to server and can expire; localStorage persists; sessionStorage is tab-scoped.', 10),
            ('What is CSS specificity and how is it calculated?', 'specificity,selector,id,class,element,cascade,priority,weight', 'Specificity determines which CSS rule applies: inline > id > class > element.', 10),
            ('What is a Single Page Application (SPA)?', 'SPA,single,page,application,React,Vue,Angular,routing,dynamic', 'SPAs load once and update content dynamically via JavaScript without full page reloads.', 10),
            ('What is the difference between null and undefined in JavaScript?', 'null,undefined,JavaScript,type,value,assigned,declared,difference', 'undefined means a variable is declared but not assigned; null is an intentional empty value.', 10),
        ],
        'hard': [
            ('Explain JavaScript\'s event loop and asynchronous programming.', 'event loop,async,callback,promise,await,non-blocking,queue,stack', 'The event loop processes the call stack and callback queue, enabling non-blocking I/O.', 15),
            ('What is WebSocket and how does it differ from HTTP?', 'WebSocket,HTTP,full-duplex,persistent,real-time,connection,upgrade,protocol', 'WebSocket provides full-duplex persistent connections, unlike HTTP\'s request-response model.', 15),
            ('Explain the Critical Rendering Path in browsers.', 'critical,rendering,path,DOM,CSSOM,render tree,layout,paint,browser', 'The CRP: parse HTML→DOM, parse CSS→CSSOM, combine→render tree, layout, paint.', 15),
            ('What is a Service Worker and what can it do?', 'service worker,PWA,cache,offline,background,fetch,push,notification', 'Service workers run in the background, enabling offline caching, push notifications, and background sync.', 15),
            ('What is Content Security Policy (CSP)?', 'CSP,security,policy,XSS,header,directive,script,source', 'CSP is an HTTP header that restricts resource sources to prevent XSS and injection attacks.', 15),
            ('Explain JavaScript\'s prototype chain and inheritance.', 'prototype,chain,inheritance,__proto__,Object,class,extends,lookup', 'JS uses prototype chains for inheritance; objects delegate property lookup up the chain.', 15),
            ('What is tree shaking in JavaScript bundlers?', 'tree shaking,dead code,webpack,rollup,ES modules,bundle,optimization,import', 'Tree shaking removes unused code (dead code elimination) from ES module bundles.', 15),
            ('What is the difference between SSR, SSG, and CSR?', 'SSR,SSG,CSR,server,static,client,rendering,Next.js,performance', 'SSR renders on server per request; SSG pre-renders at build time; CSR renders in the browser.', 15),
            ('What are Web Vitals and why do they matter?', 'Web Vitals,LCP,FID,CLS,performance,Google,Core,user experience', 'Core Web Vitals (LCP, FID, CLS) measure loading, interactivity, and visual stability for UX.', 15),
            ('Explain how browser caching works.', 'cache,Cache-Control,ETag,Last-Modified,max-age,stale,revalidate,browser', 'Browsers cache resources using Cache-Control headers, ETags, and Last-Modified for revalidation.', 15),
        ],
    },
}


class Command(BaseCommand):
    help = 'Seed the database with 30 questions per category (10 per level)'

    def add_arguments(self, parser):
        parser.add_argument('--flush', action='store_true', help='Delete existing questions first')

    def handle(self, *args, **options):
        if options['flush']:
            Question.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write('Flushed existing data.')

        self.stdout.write(self.style.WARNING('Seeding interview data...'))

        diff_map = {'easy': 'easy', 'medium': 'medium', 'hard': 'hard'}

        for cat_data in CATEGORIES:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'], defaults=cat_data
            )
            if not created:
                for k, v in cat_data.items():
                    setattr(category, k, v)
                category.save()
            self.stdout.write(f'  {"Created" if created else "Updated"}: {category.name}')

            slug = cat_data['slug']
            if slug not in QUESTIONS:
                continue

            order = 1
            for difficulty, qlist in QUESTIONS[slug].items():
                for (text, keywords, explanation, points) in qlist:
                    q, q_created = Question.objects.get_or_create(
                        category=category,
                        text=text,
                        defaults={
                            'difficulty': difficulty,
                            'correct_answer': keywords,
                            'explanation': explanation,
                            'points': points,
                            'order': order,
                        }
                    )
                    if q_created:
                        self.stdout.write(f'    + [{difficulty}] {text[:55]}...')
                    order += 1

        self.stdout.write(self.style.SUCCESS('\nDatabase seeded successfully!'))
        total = Question.objects.count()
        self.stdout.write(self.style.SUCCESS(f'Total questions: {total}'))
