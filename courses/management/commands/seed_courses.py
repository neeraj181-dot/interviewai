from django.core.management.base import BaseCommand
from courses.models import CourseTrack, CourseQuestion

TRACKS = [
    # Programming
    {'name':'Python','slug':'python','track':'programming','icon':'fab fa-python','color':'#00d4ff','description':'Master Python from basics to advanced concepts','order':1},
    {'name':'Django','slug':'django','track':'programming','icon':'fas fa-server','color':'#00ff88','description':'Django web framework — ORM, views, APIs and more','order':2},
    {'name':'JavaScript','slug':'javascript','track':'programming','icon':'fab fa-js','color':'#ffd700','description':'Modern JavaScript, ES6+, async patterns','order':3},
    {'name':'React','slug':'react','track':'programming','icon':'fab fa-react','color':'#61dafb','description':'React hooks, state management, component patterns','order':4},
    {'name':'Java','slug':'java','track':'programming','icon':'fab fa-java','color':'#f89820','description':'Core Java, OOP, collections, concurrency','order':5},
    {'name':'Node.js','slug':'nodejs','track':'programming','icon':'fab fa-node-js','color':'#68a063','description':'Server-side JavaScript with Node.js and Express','order':6},
    {'name':'C++','slug':'cpp','track':'programming','icon':'fas fa-code','color':'#9b59b6','description':'C++ fundamentals, STL, memory management','order':7},
    {'name':'Data Structures & Algorithms','slug':'dsa','track':'programming','icon':'fas fa-project-diagram','color':'#e74c3c','description':'Arrays, trees, graphs, sorting, dynamic programming','order':8},
    # AI & Future Tech
    {'name':'Machine Learning','slug':'ml','track':'ai','icon':'fas fa-brain','color':'#ff6b9d','description':'Supervised, unsupervised learning, model evaluation','order':1},
    {'name':'AI Engineering','slug':'ai-engineering','track':'ai','icon':'fas fa-robot','color':'#7b68ee','description':'LLMs, RAG, embeddings, AI system design','order':2},
    {'name':'Prompt Engineering','slug':'prompt-engineering','track':'ai','icon':'fas fa-magic','color':'#00d4ff','description':'Effective prompting, chain-of-thought, few-shot learning','order':3},
    {'name':'Data Science','slug':'data-science','track':'ai','icon':'fas fa-chart-bar','color':'#00ff88','description':'Statistics, pandas, visualization, feature engineering','order':4},
    {'name':'Cybersecurity','slug':'cybersecurity','track':'ai','icon':'fas fa-shield-alt','color':'#ff4757','description':'Security fundamentals, threats, cryptography, ethical hacking','order':5},
    # Placement Prep
    {'name':'HR Interview','slug':'hr','track':'placement','icon':'fas fa-users','color':'#ff6b9d','description':'Behavioral, situational and soft-skills questions','order':1},
    {'name':'Aptitude','slug':'aptitude','track':'placement','icon':'fas fa-calculator','color':'#ffd700','description':'Quantitative, logical reasoning, verbal ability','order':2},
    {'name':'Communication Skills','slug':'communication','track':'placement','icon':'fas fa-comments','color':'#00d4ff','description':'Verbal, written, presentation and interpersonal skills','order':3},
    {'name':'Resume Building','slug':'resume','track':'placement','icon':'fas fa-file-alt','color':'#00ff88','description':'Crafting ATS-friendly resumes and cover letters','order':4},
]

QUESTIONS = {
'python': {
'easy':[
('What is Python and what are its key features?','interpreted,dynamic,readable,versatile,open-source','Python is a high-level, interpreted, dynamically typed language known for readability.',8),
('What is the difference between a list and a tuple?','mutable,immutable,list,tuple,changeable','Lists are mutable; tuples are immutable after creation.',8),
('What are Python list comprehensions?','list,comprehension,concise,loop,expression','List comprehensions: [x*2 for x in range(10)].',8),
("Explain Python's *args and **kwargs.",'args,kwargs,variable,arguments,positional,keyword','*args collects positional args; **kwargs collects keyword args.',8),
('What is the difference between == and is?','equality,identity,value,object,reference','== checks value equality; is checks object identity.',8),
("How do you handle exceptions in Python?",'try,except,finally,raise,exception','Use try/except blocks; finally for cleanup; raise to throw.',8),
('What is a Python dictionary?','dictionary,dict,key,value,mapping,hash','A dict is a mutable key-value mapping. Access with dict[key].',8),
('What are Python built-in data types?','int,float,str,list,tuple,dict,set,bool','Built-ins: int, float, str, list, tuple, dict, set, bool, NoneType.',8),
('What is a Python module?','module,import,from,package,namespace,file','A module is a .py file. Import with import module or from module import name.',8),
('What is the difference between range() and xrange()?','range,Python 3,iterator,memory','In Python 3, range() returns an iterator. xrange() no longer exists.',8),
],
'medium':[
("What is a Python decorator?",'decorator,function,wrapper,@,higher-order,closure','A decorator wraps a function to extend its behavior using @ syntax.',10),
("What is a Python generator and yield?",'generator,yield,iterator,lazy,memory','Generators use yield to produce values lazily, saving memory.',10),
("What is the difference between __str__ and __repr__?",'str,repr,readable,developer,dunder','__str__ is human-readable; __repr__ is for debugging.',10),
('What is the difference between deep copy and shallow copy?','deep,shallow,copy,reference,nested','Shallow copy references nested objects; deep copy creates independent copies.',10),
("Explain Python's context managers.",'context,manager,with,__enter__,__exit__,resource','Context managers handle setup/teardown via __enter__/__exit__.',10),
("What are Python's magic/dunder methods?",'dunder,magic,__init__,__str__,__len__,special','Dunder methods define object behavior for built-in operations.',10),
('What is the difference between classmethod and staticmethod?','classmethod,staticmethod,cls,self,decorator','@classmethod receives cls; @staticmethod has no implicit first argument.',10),
("How does Python's garbage collection work?",'garbage,collection,reference,counting,cyclic,gc','Python uses reference counting plus a cyclic garbage collector.',10),
('What is a lambda function?','lambda,anonymous,function,expression,inline','A lambda is an anonymous single-expression function: lambda x: x*2.',10),
("Explain map(), filter(), and reduce().",'map,filter,reduce,functional,iterable','map applies a function; filter selects items; reduce folds into one value.',10),
],
'hard':[
("Explain Python's GIL.",'GIL,thread,mutex,CPython,concurrency,lock','The GIL is a CPython mutex allowing only one thread to execute bytecode at a time.',15),
('What are Python metaclasses?','metaclass,type,class,creation,__new__,customize','Metaclasses are classes of classes, controlling class creation.',15),
("Explain Python's descriptor protocol.",'descriptor,__get__,__set__,__delete__,property','Descriptors define __get__, __set__, __delete__ to customize attribute access.',15),
('What is the difference between multiprocessing and multithreading?','multiprocessing,multithreading,GIL,process,thread,parallel','Multiprocessing bypasses the GIL; threading shares memory but is GIL-limited.',15),
("Explain Python's asyncio and async/await.",'asyncio,async,await,coroutine,event loop,non-blocking','asyncio enables concurrent I/O via coroutines and an event loop.',15),
("What are Python __slots__?",'__slots__,memory,attribute,dict,optimization','__slots__ replaces __dict__, reducing memory for fixed-attribute classes.',15),
('Explain MRO in Python.','MRO,C3,linearization,multiple inheritance,super','MRO uses C3 linearization for method lookup in multiple inheritance.',15),
('What is a Python abstract base class?','ABC,abstract,base,class,abstractmethod,enforce','ABCs define interfaces using @abstractmethod, enforcing subclass implementation.',15),
("How does Python's import system work?",'import,sys.modules,finder,loader,__init__,package','Python checks sys.modules cache, then uses finders/loaders to execute module code.',15),
('What are Python weak references?','weakref,weak,reference,garbage,collection,cache','Weak references do not prevent garbage collection; useful for caches.',15),
],
},
'javascript': {
'easy':[
('What is JavaScript and where is it used?','scripting,browser,server,dynamic,web,Node','JavaScript is a scripting language used for web interactivity and server-side with Node.js.',8),
('What is the difference between var, let, and const?','var,let,const,scope,hoisting,block,function','var is function-scoped and hoisted; let/const are block-scoped; const cannot be reassigned.',8),
('What is the DOM?','DOM,document,object,model,tree,node,element','The DOM is a tree representation of HTML that JavaScript can manipulate.',8),
('What is the difference between == and ===?','equality,strict,type,coercion,===,==','== coerces types before comparing; === checks value and type strictly.',8),
('What are JavaScript data types?','string,number,boolean,null,undefined,object,symbol,bigint','JS types: string, number, boolean, null, undefined, object, symbol, BigInt.',8),
('What is a JavaScript function?','function,declaration,expression,arrow,invoke,return','Functions are reusable blocks of code defined with function keyword or arrow syntax.',8),
('What is an array in JavaScript?','array,list,index,push,pop,map,filter,ordered','Arrays are ordered lists accessed by index with methods like push, pop, map, filter.',8),
('What is the difference between null and undefined?','null,undefined,assigned,declared,intentional','undefined means declared but not assigned; null is an intentional empty value.',8),
('What is a JavaScript object?','object,key,value,property,method,literal,{}','Objects are key-value pairs. Created with {} or new Object().',8),
('What is event handling in JavaScript?','event,listener,addEventListener,click,DOM,handler','Events are user actions; addEventListener attaches handlers to DOM elements.',8),
],
'medium':[
("Explain JavaScript's event loop.",'event loop,async,callback,promise,await,non-blocking,queue','The event loop processes the call stack and callback queue for non-blocking I/O.',10),
('What is a JavaScript Promise?','promise,async,resolve,reject,then,catch,pending','A Promise represents an async operation with states: pending, fulfilled, rejected.',10),
('What is async/await in JavaScript?','async,await,promise,asynchronous,syntax,cleaner','async/await is syntactic sugar over Promises for cleaner async code.',10),
('What is closure in JavaScript?','closure,scope,inner,outer,function,variable,lexical','A closure is a function that retains access to its outer scope variables.',10),
('What is the difference between call, apply, and bind?','call,apply,bind,this,context,arguments','call/apply invoke immediately with a this context; bind returns a new function.',10),
('What is prototypal inheritance?','prototype,chain,inheritance,__proto__,Object,lookup','JS uses prototype chains; objects delegate property lookup up the chain.',10),
('What is destructuring in JavaScript?','destructuring,array,object,extract,assign,ES6','Destructuring extracts values from arrays/objects into variables.',10),
('What are JavaScript modules?','module,import,export,ES6,CommonJS,namespace','ES6 modules use import/export to share code between files.',10),
('What is the spread operator?','spread,...,array,object,copy,merge,ES6','The spread operator (...) expands iterables into individual elements.',10),
('What is a higher-order function?','higher-order,function,map,filter,reduce,callback,argument','A higher-order function takes or returns another function.',10),
],
'hard':[
('Explain JavaScript memory management.','memory,heap,stack,garbage,collection,leak,reference','JS uses automatic garbage collection; memory leaks occur with lingering references.',15),
('What is the difference between microtasks and macrotasks?','microtask,macrotask,queue,promise,setTimeout,event loop','Microtasks (Promises) run before macrotasks (setTimeout) in the event loop.',15),
('What is a WeakMap and WeakSet?','WeakMap,WeakSet,weak,reference,garbage,collection,key','WeakMap/WeakSet hold weak references, allowing garbage collection of keys.',15),
('Explain JavaScript generators.','generator,function*,yield,iterator,lazy,next','Generators use function* and yield to produce values lazily on demand.',15),
('What is the Proxy object in JavaScript?','Proxy,handler,trap,get,set,intercept,meta','Proxy intercepts object operations via handler traps for get, set, etc.',15),
('What is tree shaking?','tree shaking,dead code,webpack,rollup,ES modules,bundle','Tree shaking removes unused code from ES module bundles at build time.',15),
('Explain JavaScript design patterns.','design pattern,singleton,observer,factory,module,MVC','Common patterns: Singleton, Observer, Factory, Module, MVC for code organization.',15),
('What is the difference between SSR, SSG, and CSR?','SSR,SSG,CSR,server,static,client,rendering,Next.js','SSR renders per request; SSG pre-renders at build; CSR renders in browser.',15),
('What are Web Workers?','Web Worker,thread,background,parallel,message,postMessage','Web Workers run scripts in background threads without blocking the main thread.',15),
('Explain JavaScript security best practices.','XSS,CSRF,sanitize,CSP,HTTPS,input,validation','Prevent XSS by sanitizing input; use CSP headers; validate all user data.',15),
],
},
'ml': {
'easy':[
('What is Machine Learning?','supervised,unsupervised,reinforcement,data,model,predict','ML is a subset of AI where systems learn from data to make predictions.',8),
('What is the difference between supervised and unsupervised learning?','supervised,unsupervised,labeled,unlabeled,classification,clustering','Supervised uses labeled data; unsupervised finds patterns in unlabeled data.',8),
('What is a training set and test set?','training,test,split,evaluate,generalize,overfitting','Training set trains the model; test set evaluates its generalization.',8),
('What is overfitting?','overfitting,training,generalize,noise,regularization,complex','Overfitting is when a model learns noise in training data and fails to generalize.',8),
('What is a feature in ML?','feature,input,variable,attribute,column,predictor','A feature is an input variable used to make predictions.',8),
('What is a classification problem?','classification,label,category,predict,class,output','Classification predicts discrete categories (e.g., spam/not spam).',8),
('What is regression in ML?','regression,continuous,predict,output,linear,value','Regression predicts continuous values (e.g., house prices).',8),
('What is a confusion matrix?','confusion,matrix,TP,FP,TN,FN,accuracy,precision,recall','A confusion matrix shows TP, FP, TN, FN to evaluate classification models.',8),
('What is cross-validation?','cross-validation,k-fold,evaluate,generalize,split,bias','Cross-validation splits data into k folds to evaluate model performance reliably.',8),
('What is the bias-variance tradeoff?','bias,variance,tradeoff,underfitting,overfitting,balance','High bias = underfitting; high variance = overfitting. Balance is key.',8),
],
'medium':[
('What is gradient descent?','gradient,descent,optimization,loss,learning rate,minimize','Gradient descent minimizes loss by iteratively updating parameters in the gradient direction.',10),
('What is regularization in ML?','regularization,L1,L2,lasso,ridge,overfitting,penalty','Regularization adds a penalty to prevent overfitting: L1 (Lasso), L2 (Ridge).',10),
('What is a decision tree?','decision,tree,split,node,leaf,entropy,gini,classification','Decision trees split data on features to create a tree of decisions.',10),
('What is a random forest?','random,forest,ensemble,bagging,trees,variance,accuracy','Random forest is an ensemble of decision trees using bagging to reduce variance.',10),
('What is SVM?','SVM,support,vector,machine,hyperplane,margin,kernel','SVM finds the optimal hyperplane that maximizes the margin between classes.',10),
('What is k-means clustering?','k-means,clustering,centroid,unsupervised,distance,assign','k-means assigns data points to k clusters based on distance to centroids.',10),
('What is PCA?','PCA,principal,component,analysis,dimensionality,reduction,variance','PCA reduces dimensionality by projecting data onto principal components.',10),
('What is the difference between precision and recall?','precision,recall,F1,TP,FP,FN,tradeoff','Precision = TP/(TP+FP); Recall = TP/(TP+FN). F1 balances both.',10),
('What is feature engineering?','feature,engineering,transform,create,select,improve,model','Feature engineering creates or transforms features to improve model performance.',10),
('What is a neural network?','neural,network,neuron,layer,activation,weights,backprop','Neural networks are layers of neurons with weights trained via backpropagation.',10),
],
'hard':[
('What is backpropagation?','backpropagation,gradient,chain rule,weights,update,loss','Backprop computes gradients via chain rule to update network weights.',15),
('What is the vanishing gradient problem?','vanishing,gradient,deep,network,sigmoid,ReLU,training','Gradients shrink in deep networks; ReLU and batch norm help mitigate this.',15),
('What is transfer learning?','transfer,learning,pretrained,fine-tune,features,domain','Transfer learning reuses a pretrained model and fine-tunes it for a new task.',15),
('What is attention mechanism in transformers?','attention,transformer,self-attention,query,key,value,BERT','Attention computes weighted sums of values based on query-key similarity.',15),
('What is the difference between CNN and RNN?','CNN,RNN,convolutional,recurrent,image,sequence,spatial,temporal','CNNs process spatial data (images); RNNs process sequential data (text, time series).',15),
('What is reinforcement learning?','reinforcement,agent,environment,reward,policy,Q-learning','RL trains agents to maximize cumulative reward through environment interaction.',15),
('What is batch normalization?','batch,normalization,training,stability,internal,covariate,shift','Batch norm normalizes layer inputs to stabilize and accelerate training.',15),
('What is dropout regularization?','dropout,regularization,overfitting,random,neurons,training','Dropout randomly deactivates neurons during training to prevent overfitting.',15),
('What is the difference between GAN and VAE?','GAN,VAE,generative,adversarial,variational,autoencoder,latent','GANs use adversarial training; VAEs use variational inference for generation.',15),
('What is hyperparameter tuning?','hyperparameter,tuning,grid search,random search,Bayesian,optimize','Hyperparameter tuning finds optimal model settings via grid/random/Bayesian search.',15),
],
},
'hr': {
'easy':[
('Tell me about yourself.','experience,skills,background,professional,career,education','Cover education, experience, key skills, and career goals concisely.',8),
('What are your greatest strengths?','strength,skill,quality,asset,relevant,example','Mention 2-3 genuine strengths relevant to the role with brief examples.',8),
('Why do you want to work here?','company,culture,mission,values,opportunity,growth,research','Research the company and align your answer with their mission and the role.',8),
('Where do you see yourself in 5 years?','goal,growth,career,future,develop,leadership,ambition','Show ambition aligned with the company growth and your development.',8),
('What motivates you?','motivate,passion,challenge,learn,achieve,impact,growth','Be authentic — mention learning, impact, and problem-solving.',8),
('What is your greatest weakness?','weakness,improve,honest,growth,learning,working,overcome','Mention a real weakness you are actively working to improve.',8),
('Why are you leaving your current job?','leaving,reason,growth,opportunity,challenge,positive','Stay positive — focus on growth opportunities rather than negatives.',8),
('What are your salary expectations?','salary,expectation,research,market,range,negotiate','Research market rates and give a range based on your skills.',8),
('How would your colleagues describe you?','colleague,team,describe,reliable,collaborative,feedback','Mention positive traits backed by examples: reliable, collaborative.',8),
('Do you have any questions for us?','question,culture,team,role,growth,opportunity,curious','Always ask thoughtful questions about the role, team, or growth.',8),
],
'medium':[
('Describe a challenging situation you resolved.','challenge,situation,action,result,STAR,problem,solution','Use STAR: Situation, Task, Action, Result.',10),
('How do you handle pressure and deadlines?','pressure,deadline,prioritize,manage,calm,organize,time','Describe time management strategies and give a real example.',10),
('Tell me about a time you failed.','failure,learn,mistake,recover,lesson,growth,resilience','Be honest about a real failure and focus on what you learned.',10),
('How do you prioritize multiple tasks?','prioritize,deadline,urgent,important,matrix,organize','Describe your prioritization framework with a real example.',10),
('Tell me about a time you showed leadership.','leadership,initiative,team,guide,decision,responsibility','Describe taking initiative, guiding others, and achieving results.',10),
('How do you handle conflict with a coworker?','conflict,resolve,communicate,listen,empathy,professional','Describe a calm, professional approach: listen, communicate, find common ground.',10),
('What is your approach to learning new tech?','learn,technology,adapt,course,practice,documentation','Describe your learning process: docs, courses, hands-on practice.',10),
('Tell me about a time you went above and beyond.','above,beyond,extra,initiative,impact,result,dedication','Share a specific example where you exceeded expectations.',10),
('How do you give and receive feedback?','feedback,constructive,listen,improve,specific,actionable','Describe giving specific feedback and receiving it with openness.',10),
('Describe your teamwork experience.','team,collaborate,communicate,contribute,role,cooperation','Highlight collaboration, communication, and your specific contributions.',10),
],
'hard':[
('Describe a difficult decision with incomplete information.','decision,incomplete,risk,analyze,judgment,outcome,ambiguity','Describe your decision-making process under uncertainty.',15),
('How have you managed a project end-to-end?','project,manage,plan,execute,stakeholder,timeline,deliver','Walk through planning, stakeholder management, execution, and delivery.',15),
('Tell me about influencing without authority.','influence,persuade,authority,stakeholder,communication,trust','Describe building trust and persuading without formal authority.',15),
('How do you handle disagreement with your manager?','disagree,manager,professional,communicate,respect,data','Describe respectfully presenting your perspective with data.',15),
('Describe driving significant organizational change.','change,drive,initiative,resistance,stakeholder,impact','Describe identifying the need, building buy-in, and measuring impact.',15),
('How do you build relationships with difficult stakeholders?','stakeholder,relationship,difficult,empathy,trust,communication','Describe understanding their perspective and building trust over time.',15),
('Tell me about delivering bad news.','bad news,deliver,honest,empathy,solution,professional','Describe being direct, empathetic, and solution-focused.',15),
('How do you stay current with industry trends?','industry,trend,learn,conference,publication,network,adapt','Describe reading publications, attending conferences, and networking.',15),
('Describe your approach to mentoring juniors.','mentor,junior,guide,teach,patience,growth,feedback,support','Describe understanding their goals, providing guidance, and celebrating growth.',15),
('How do you measure your own success?','success,measure,goal,KPI,impact,growth,reflection','Describe setting clear goals, tracking KPIs, and continuous improvement.',15),
],
},
}


class Command(BaseCommand):
    help = 'Seed courses and questions'

    def add_arguments(self, parser):
        parser.add_argument('--flush', action='store_true', help='Delete existing data first')

    def handle(self, *args, **options):
        if options['flush']:
            CourseQuestion.objects.all().delete()
            CourseTrack.objects.all().delete()
            self.stdout.write('Flushed course data.')

        self.stdout.write(self.style.WARNING('Seeding courses...'))

        for t in TRACKS:
            track, created = CourseTrack.objects.get_or_create(slug=t['slug'], defaults=t)
            if not created:
                for k, v in t.items():
                    setattr(track, k, v)
                track.save()
            self.stdout.write(f'  {"+" if created else "~"} {track.name}')

            slug = t['slug']
            if slug not in QUESTIONS:
                continue

            order = 1
            for difficulty, qlist in QUESTIONS[slug].items():
                for (text, keywords, explanation, points) in qlist:
                    q, q_created = CourseQuestion.objects.get_or_create(
                        course=track, text=text,
                        defaults={'difficulty': difficulty, 'correct_answer': keywords,
                                  'explanation': explanation, 'points': points, 'order': order}
                    )
                    if q_created:
                        self.stdout.write(f'    + [{difficulty}] {text[:55]}')
                    order += 1

        total = CourseQuestion.objects.count()
        self.stdout.write(self.style.SUCCESS(f'\nDone! Total course questions: {total}'))
