"""
Examples for categories to classify stage directions against.

The mention to "detailed" in variable names refers to including expressions related to labels from FreDraCor annotations in the category definitions used in the propmts.

We have the following variables:

- defs_detailed_en: Detailed definitions only ("detailed" in the sense described above), in English
- defs_detailed_fr: Detailed definitions only, in French
- two_shot_fr_en: Definitions (without details) in English and two or three examples for each language
- two_shot_fr: Definitions (without details) in English and two or three examples in French only
- few_shot_defs_simple_en: Definitions (without details) in English and examples in French only,
  in a few-shot manner (so far 20 examples per category)
- few_shot_defs_detailed_en: Detailed definitions in English and examples in French only,
  in a few-shot manner (so far 20 examples per category)
- few_shot_defs_detailed_fr: Detailed definitions in French and examples in French only,
  in a few-shot manner (so far 20 examples per category)
"""


# ENGLISH PROMPTS -------------------------------------------------------------

# Detailed definition, no examples
defs_detailed_en = """
- Category 0
  - Name: action
  - Definition: General character action. Use it only when other categories do not describe the action. Verbs related to this category are watch, show, paint, pray, jump, read, kneel, fall, knock, write, drink, search, open, eat, sleep, stand, sit, move, listen, ring among others.
- Category 1
  - Name: aggression
  - Definition: Violent action. Related to notions like kill, fight, hit, suicide or threat.
- Category 2
  - Name: aparte
  - Definition: Aside (character addresses audience or is alone).
- Category 3
  - Name: delivery
  - Definition: Delivery manner, e.g. regarding voice or vocal expression of emotion. Also used when the character sings. Can refer to notions like the character showing anger or being furious, being serious, happy, hesitant, showing enthousiasm, emotion, emphasis, being friendly, making a grimace, showing a feeling, or repeating an expression.
- Category 4
  - Name: entrance
  - Definition: Character enters stage.
- Category 5
  - Name: exit
  - Definition: Character exits. Verbs related to this type of stage direction are (in French) "se retirer", "sortir", "s'en aller" and other close verbs.
- Category 6
  - Name: interaction
  - Definition: Non-verbal character interaction. The interaction must be non-verbal, e.g. looking at, pointing at, touching, helping, pulling, pushing among other non-verbal interaction types.
- Category 7
  - Name: movement
  - Definition: Character movement (but not exit/entrance). Sometimes related to getting closer, moving away, walking away, following a character, moving back.
- Category 8
  - Name: music
  - Definition: Tune names (plays with songs). Music description. Not used when the stage direction describes the character singing. Often starts with the word "AIR" or "Air". If it starts with these words, it is most likely a music stage direction and the content following these words is the name of the tune.
- Category 9
  - Name: narration
  - Definition: Long stage direction, with narrative quality, inteded for readers. Generally long stage directions, they can narrate a sequence of character actions. They can also refer to noises or to weather events.
- Category 10
  - Name: object
  - Definition: Describes an object or a character's interaction with an object, including giving or receiving an object or otherwise handling or manipulating the object, among other interactions. The object may be a costume or a dress for instance. Verbs related to this category are throw, tear, get, give, dress, drop, close among others. 
- Category 11
  - Name: setting
  - Definition: Stage description or play location.
- Category 12
  - Name: toward
  - Definition: Indicates the addressee of a speech.

"""

# Two shot (definition without details), two to three examples
two_shot_fr_en = """
- Category 0
  - Name: action
  - Definition: General character action
  - Examples
    - Example 1: Il désigne le garçon de café
    - Example 2: Il lit
    - Example 3: Elle s'assied
    - Example 4: He points to the waiter
    - Example 5: He reads
    - Example 6: She sits down
- Category 1
  - Name: aggression
  - Definition: Violent action
  - Examples
    - Example 1: Il tire son épée
    - Example 2: Il se donne un coup
    - Example 3: He draws his sword
    - Example 4: He strikes himself
- Category 2
  - Name: aparte
  - Definition: Aside (character addresses audience or is alone)
  - Examples
    - Example 1: À part
    - Example 2: Seule
    - Example 3: Aside
    - Example 4: Alone
- Category 3
  - Name: delivery
  - Definition: Delivery manner, e.g. regarding voice or vocal expression of emotion
  - Examples
      - Example 1: En riant
      - Example 2: À demi-voix
      - Example 3: Laughing
      - Example 4: In a low voice
- Category 4
  - Name: entrance
  - Definition: Character enters stage
  - Examples
    - Example 1: Ils entrent en scène
    - Example 2: Il rentre chez lui
    - Example 3: They enter the stage
    - Example 4: He enters his home
- Category 5
  - Name: exit
  - Definition: Character exits
  - Examples
    - Example 1: Il sort
    - Example 2: Il rentre
    - Example 3: She exits
    - Example 4: He re-enters
- Category 6
  - Name: interaction
  - Definition: Non-verbal character interaction
  - Examples
    - Example 1: Elle va aussi pour l’embrasser
    - Example 2: Elle prend sa main
    - Example 3: She moves to kiss him
    - Example 4: He takes her hand
- Category 7
  - Name: movement
  - Definition: Character movement (but not exit/entrance)
  - Examples
    - Example 1: Il continue sa marche
    - Example 2: Il recule d’un autre côté
    - Example 3: Il veut sortir
    - Example 4: He continues his walk
    - Example 5: He retreats to the other side
    - Example 6: He wants to exit
- Category 8
  - Name: music
  - Definition: Tune names (plays with songs); music description
  - Examples
    - Example 1: Air en duo
    - Example 2: Musique céleste
    - Example 3: Duet melody
    - Example 4: Celestial music
- Category 9
  - Name: narration
  - Definition: Long stage direction, with narrative quality, inteded for readers
  - Examples
    - Example 1: Cependant VENDE, qui avait été mandée, survient après les acclamations du peuple, elle commande à son Chancelier de déclarer ses intentions à l’Assemblée
    - Example 2: Cette scène est très divertissante, et jouée parfaitement par le Pédant, qui devient amoureux à son tour de Colombine. D'abord il lui donne un mouchoir pour cacher sa gorge ; mais incontinent il se laisse entraîner au pouvoir de l'amour. L'écolier survient qui voit le Pédant embrasser Colombine : il lui rend avec usure les coups de bâton ; ce qui finit la scène.
    - Example 3: Pendant le dernier couplet, la force armée est entrée et a passé devant les citoyens, de manière que les jacobins quiont tous la figure du côté du public, ne peuvent la voir à la fin du couplet.
    - Example 4: However, VENDE, who had been summoned, appears after the cheers of the people; she commands her Chancellor to declare her intentions to the Assembly
    - Example 5: This scene is very entertaining, and perfectly played by the Pedant, who in turn falls in love with Columbine. At first he gives her a handkerchief to hide her throat; but immediately he lets himself be carried away by the power of love. The schoolboy arrives who sees the Pedant kissing Columbine: he returns the blows with the stick with usury; which ends the scene.
    - Example 6: During the last verse, the armed force entered and passed in front of the citizens, so that the Jacobins, who all had their faces on the side of the audience, could not see it at the end of the verse.
- Category 10
  - Name: object
  - Definition: Describes an object or interaction with it
  - Examples
    - Example 1: Il lui donne un écu
    - Example 2: Elle froisse la lettre
    - Example 3: He gives her a coin
    - Example 4: She crumples the letter
- Category 11
  - Name: setting
  - Definition: Stage description or play location
  - Examples
    - Example 1: Le théâtre représente un salon
    - Example 2: À Sicilie
    - Example 3: The theater represents a living room
    - Example 4: In Sicily
- Category 12
  - Name: Toward
  - Definition: Indicates the addressee of a speech
  - Examples
    - Example 1: À Julie
    - Example 2: Au commandeur et au comte
    - Example 3: Toward Julie
    - Example 4: To the commander and the count

"""

two_shot_fr = """
- Category 0
  - Name: action
  - Definition: General character action
  - Examples
    - Example 1: Il désigne le garçon de café
    - Example 2: Il lit
    - Example 3: Elle s'assied
- Category 1
  - Name: aggression
  - Definition: Violent action
  - Examples
    - Example 1: Il tire son épée
    - Example 2: Il se donne un coup
- Category 2
  - Name: aparte
  - Definition: Aside (character addresses audience or is alone)
  - Examples
    - Example 1: À part
    - Example 2: Seule
- Category 3
  - Name: delivery
  - Definition: Delivery manner, e.g. regarding voice or vocal expression of emotion
  - Examples
      - Example 1: En riant
      - Example 2: À demi-voix
- Category 4
  - Name: entrance
  - Definition: Character enters stage
  - Examples
    - Example 1: Ils entrent en scène
    - Example 2: Il rentre chez lui
- Category 5
  - Name: exit
  - Definition: Character exits
  - Examples
    - Example 1: Il sort
    - Example 2: Il rentre
- Category 6
  - Name: interaction
  - Definition: Non-verbal character interaction
  - Examples
    - Example 1: Elle va aussi pour l’embrasser
    - Example 2: Elle prend sa main
- Category 7
  - Name: movement
  - Definition: Character movement (but not exit/entrance)
  - Examples
    - Example 1: Il continue sa marche
    - Example 2: Il recule d’un autre côté
    - Example 3: Il veut sortir
- Category 8
  - Name: music
  - Definition: Tune names (plays with songs); music description
  - Examples
    - Example 1: Air en duo
    - Example 2: Musique céleste
- Category 9
  - Name: narration
  - Definition: Long stage direction, with narrative quality, inteded for readers
  - Examples
    - Example 1: Cependant VENDE, qui avait été mandée, survient après les acclamations du peuple, elle commande à son Chancelier de déclarer ses intentions à l’Assemblée
    - Example 2: Cette scène est très divertissante, et jouée parfaitement par le Pédant, qui devient amoureux à son tour de Colombine. D'abord il lui donne un mouchoir pour cacher sa gorge ; mais incontinent il se laisse entraîner au pouvoir de l'amour. L'écolier survient qui voit le Pédant embrasser Colombine : il lui rend avec usure les coups de bâton ; ce qui finit la scène.
    - Example 3: Pendant le dernier couplet, la force armée est entrée et a passé devant les citoyens, de manière que les jacobins quiont tous la figure du côté du public, ne peuvent la voir à la fin du couplet.
- Category 10
  - Name: object
  - Definition: Describes object or interaction with it
  - Examples
    - Example 1: Il lui donne un écu
    - Example 2: Elle froisse la lettre
- Category 11
  - Name: setting
  - Definition: Stage description or play location
  - Examples
    - Example 1: Le théâtre représente un salon
    - Example 2: À Sicilie
- Category 12
  - Name: toward
  - Definition: Indicates the addressee of a speech
  - Examples
    - Example 1: À Julie
    - Example 2: Au commandeur et au comte
"""

# Few shot (definition without details)
few_shot_defs_simple_en = """
- CATEGORY 0
  - NAME: action
  - DEFINITION: General character action. Use it only when other categories do not describe the action. 
  - EXAMPLES:
{examples_0}
- CATEGORY 1
  - Name: aggression
  - DEFINITION: Violent action.
  - EXAMPLES:
{examples_1}
- CATEGORY 2
  - Name: aparte
  - DEFINITION: Aside (character addresses audience or is alone)
  - EXAMPLES:     
{examples_2}
- CATEGORY 3
  - NAME: delivery
  - DEFINITION: Delivery manner, e.g. regarding voice or vocal expression of emotion. Also used when the character sings. 
  - EXAMPLES: 
{examples_3}
- CATEGORY 4
  - NAME: entrance
  - DEFINITION: Character enters stage.
  - EXAMPLES: 
{examples_4}
- CATEGORY 5
  - NAME: exit
  - DEFINITION: Character exits.
  - EXAMPLES: 
{examples_5}
- CATEGORY 6
  - NAME: interaction
  - DEFINITION: Non-verbal character interaction. The interaction must be non-verbal.
  - EXAMPLES: 
{examples_6}
- CATEGORY 7
  - NAME: movement
  - DEFINITION: Character movement (but not exit/entrance).
  - EXAMPLES: 
{examples_7}
- CATEGORY 8
  - NAME: music
  - DEFINITION: Tune names (plays with songs). Music description. Not used when the stage direction describes the character singing. Often starts with the word "AIR" or "Air". If it starts with these words, it is most likely a music stage direction and the content following these words is the name of the tune.
  - EXAMPLES: 
{examples_8}
- CATEGORY 9
  - NAME: narration
  - DEFINITION: Long stage direction, with narrative quality, inteded for readers.  Generally long stage directions, they can narrate a sequence of character actions. They can also refer to noises or to weather events.
  - EXAMPLES: 
{examples_9}
- CATEGORY 10
  - NAME: object
  - DEFINITION: Describes an object or a character's interaction with an object, including giving or receiving an object or otherwise handling or manipulating the object, among other interactions. 
  - EXAMPLES: 
{examples_10}
- CATEGORY 11
  - NAME: setting
  - DEFINITION: Stage description or play location.
  - EXAMPLES: 
{examples_11}
- CATEGORY 12
  - NAME: toward
  - DEFINITION: Indicates the addressee of a speech.
  - EXAMPLES: 
{examples_12}
"""

# Few shot (detailed definitions)
few_shot_defs_detailed_en = """
- CATEGORY 0
  - NAME: action
  - DEFINITION: General character action. Use it only when other categories do not describe the action.  Verbs related to this category are watch, show, paint, pray, jump, read, kneel, fall, knock, write, drink, search, open, eat, sleep, stand, sit, move, listen, ring among others.
  - EXAMPLES:
{examples_0}
- CATEGORY 1
  - Name: aggression
  - DEFINITION: Violent action. Related to notions like kill, fight, hit, suicide or threat.
  - EXAMPLES:
{examples_1}
- CATEGORY 2
  - Name: aparte
  - DEFINITION: Aside (character addresses audience or is alone).
  - EXAMPLES:     
{examples_2}
- CATEGORY 3
  - NAME: delivery
  - DEFINITION: Delivery manner, e.g. regarding voice or vocal expression of emotion. Also used when the character sings. Can refer to notions like the character showing anger or being furious, being serious, happy, hesitant, showing enthousiasm, emotion, emphasis, being friendly, making a grimace, showing a feeling, or repeating an expression.
  - EXAMPLES: 
{examples_3}
- CATEGORY 4
  - NAME: entrance
  - DEFINITION: Character enters stage.
  - EXAMPLES: 
{examples_4}
- CATEGORY 5
  - NAME: exit
  - DEFINITION: Character exits. Verbs related to this type of stage direction are (in French) "se retirer", "sortir", "s'en aller" and other close verbs.
  - EXAMPLES: 
{examples_5}
- CATEGORY 6
  - NAME: interaction
  - DEFINITION: Non-verbal character interaction. The interaction must be non-verbal, e.g. looking at, pointing at, touching, helping, pulling, pushing among other non-verbal interaction types.
  - EXAMPLES: 
{examples_6}
- CATEGORY 7
  - NAME: movement
  - DEFINITION: Character movement (but not exit/entrance). Sometimes related to getting closer, moving away, walking away, following a character, moving back.
  - EXAMPLES: 
{examples_7}
- CATEGORY 8
  - NAME: music
  - DEFINITION: Tune names (plays with songs). Music description. Not used when the stage direction describes the character singing. Often starts with the word "AIR" or "Air". If it starts with these words, it is most likely a music stage direction and the content following these words is the name of the tune.
  - EXAMPLES: 
{examples_8}
- CATEGORY 9
  - NAME: narration
  - DEFINITION: Long stage direction, with narrative quality, inteded for readers.  Generally long stage directions, they can narrate a sequence of character actions. They can also refer to noises or to weather events.
  - EXAMPLES: 
{examples_9}
- CATEGORY 10
  - NAME: object
  - DEFINITION: Describes an object or a character's interaction with an object, including giving or receiving an object or otherwise handling or manipulating the object, among other interactions. The object may be a costume or a dress for instance. Verbs related to this category are throw, tear, get, give, dress, drop, close among others. 
  - EXAMPLES: 
{examples_10}
- CATEGORY 11
  - NAME: setting
  - DEFINITION: Stage description or play location.
  - EXAMPLES: 
{examples_11}
- CATEGORY 12
  - NAME: toward
  - DEFINITION: Indicates the addressee of a speech.
  - EXAMPLES: 
{examples_12}
"""

# FRENCH PROMPTS --------------------------------------------------------------

# Detailed definition, no examples
defs_detailed_fr = """
- Catégorie 0
  - Nom: action
  - Définition: Catégorie générale pour les actions des personnages. Utilisez cette catégorie uniquement lorsque d'autres catégories ne décrivent pas l'action. Quelques verbes liés à cette catégorie sont regarder, montrer, peindre, prier, sauter, lire, s'agenouiller, tomber, frapper, écrire, boire, chercher, ouvrir, manger, dormir, être debout, s'asseoir, bouger, écouter, sonner parmi d'autres.
- Catégorie 1
  - Nom: aggression
  - Définition: Action violente. Liée à des notions comme tuer, se battre, frapper, le suicide ou la menace.
- Catégorie 2
  - Nom: aparte
  - Définition: Aparté (le personnage s'adresse au public ou est seul).
- Catégorie 3
  - Nom: delivery
  - Définition: Décrit comment est interprétée une réplique, par exemple en ce qui concerne la voix ou l'expression vocale d'une émotion. Utilisée également lorsque le personnage chante. Peut se référer à des notions telles que le personnage montrant de la colère ou étant furieux, étant sérieux, heureux, hésitant, montrant de l'enthousiasme, de l'émotion, de l'emphase, se montrant gentil, faisant une grimace, montrant un sentiment, ou répétant une expression.
- Catégorie 4
  - Nom: entrance
  - Définition: Le personnage entre en scène.
- Catégorie 5
  - Nom: exit
  - Définition: Le personnage sort, quitte la scène.
- Catégorie 6
  - Nom: interaction
  - Définition: Interaction non verbale entre les personnages. L'interaction doit être non verbale, par exemple regarder, pointer du doigt, toucher, aider, tirer, pousser parmi d'autres types d'interactions non verbales.
- Catégorie 7
  - Nom: movement
  - Définition: Déplacement du personnage (mais pas une entrée ou sortie). Parfois lié à des notions comme s'approcher, s'éloigner, suivre un personnage, reculer.
- Catégorie 8
  - Nom: music
  - Définition:  Noms des airs (dans les pièces de théâtre avec des chansons), ou description de la musique. Catégorie non utilisée lorsque la didascalie fait référence à un personnage qui chante. La didascalie commence souvent par le mot « AIR » ou « Air ». Si la didascalie commence par ces mots, il s'agit très probablement d'une didascalie de cette catégorie, et les mots suivants constituent le nom de l'air.
- Catégorie 9
  - Nom: narration
  - Définition: Didascalie longue, à caractère narratif, à destination des lecteurs. Généralement de longues didascalies. Elles peuvent relater une séquence d'actions des personnages. Elles peuvent également faire référence à des bruits ou à des phénomènes météorologiques.
- Catégorie 10
  - Nom: object
  - Définition: Décrit un objet ou l'interaction d'un personnage avec un objet, y compris donner ou recevoir un objet ou manipuler l'objet de quelque manière que ce soit, entre autres interactions. L'objet peut être des vêtements, des costumes. Quelques verbes liés à cette catégorie sont jeter, déchirer, obtenir, donner, habiller, laisser tomber, fermer parmi d'autres.
- Catégorie 11
  - Nom: setting
  - Définition: Description de la scène ou lieu de la pièce.
- Catégorie 12
  - Nom: toward
  - Définition: Indique le destinataire d'une réplique.

"""

# Few shot (definition without details)
few_shot_defs_simple_fr = """
- CATÉGORIE 0
  - NOM: action
  - DÉFINITION: Catégorie générale pour les actions des personnages. Utilisez cette catégorie uniquement lorsque d'autres catégories ne décrivent pas l'action.
  - EXEMPLES:
{examples_0}
- CATÉGORIE 1
  - NOM: aggression
  - DÉFINITION: Action violente.
  - EXEMPLES:
{examples_1}
- CATÉGORIE 2
  - NOM: aparte
  - DÉFINITION: Aparté (le personnage s'adresse au public ou est seul).
  - EXEMPLES:     
{examples_2}
- CATÉGORIE 3
  - NOM: delivery
  - DÉFINITION: Décriqt comment est interprétée une réplique, par exemple en ce qui concerne la voix ou l'expression vocale d'une émotion. Utilisée également lorsque le personnage chante.
  - EXEMPLES: 
{examples_3}
- CATÉGORIE 4
  - NOM: entrance
  - DÉFINITION: Le personnage entre en scène.
  - EXEMPLES: 
{examples_4}
- CATÉGORIE 5
  - NOM: exit
  - DÉFINITION: Le personnage sort, quitte la scène.
  - EXEMPLES: 
{examples_5}
- CATÉGORIE 6
  - NOM: interaction
  - DÉFINITION: Interaction non verbale entre les personnages. L'interaction doit être non verbale.
  - EXEMPLES: 
{examples_6}
- CATÉGORIE 7
  - NOM: movement
  - DÉFINITION: Déplacement du personnage (mais pas une entrée ou sortie).
  - EXEMPLES: 
{examples_7}
- CATÉGORIE 8
  - NOM: music
  - DÉFINITION: Noms des airs (dans les pièces de théâtre avec des chansons), ou description de la musique. Catégorie non utilisée lorsque la didascalie fait référence à un personnage qui chante. La didascalie commence souvent par le mot « AIR » ou « Air ». Si la didascalie commence par ces mots, il s'agit très probablement d'une didascalie de cette catégorie, et les mots suivants constituent le nom de l'air.
  - EXEMPLES: 
{examples_8}
- CATÉGORIE 9
  - NOM: narration
  - DÉFINITION: Didascalie longue, à caractère narratif, à destination des lecteurs. Généralement de longues didascalies. Elles peuvent relater une séquence d'actions des personnages. Elles peuvent également faire référence à des bruits ou à des phénomènes météorologiques.
  - EXEMPLES: 
{examples_9}
- CATÉGORIE 10
  - NOM: object
  - DÉFINITION: Décrit un objet ou l'interaction d'un personnage avec un objet, y compris donner ou recevoir un objet ou manipuler l'objet de quelque manière que ce soit, entre autres interactions.
  - EXEMPLES: 
{examples_10}
- CATÉGORIE 11
  - NOM: setting
  - DÉFINITION: Description de la scène ou lieu de la pièce.
  - EXEMPLES: 
{examples_11}
- CATÉGORIE 12
  - NOM: toward
  - DÉFINITION: Indique le destinataire d'une réplique.
  - EXEMPLES: 
{examples_12}

"""

# Few shot (detailed definitions)
few_shot_defs_detailed_fr = """
- CATÉGORIE 0
  - NOM: action
  - DÉFINITION: Catégorie générale pour les actions des personnages. Utilisez cette catégorie uniquement lorsque d'autres catégories ne décrivent pas l'action. Quelques verbes liés à cette catégorie sont regarder, montrer, peindre, prier, sauter, lire, s'agenouiller, tomber, frapper, écrire, boire, chercher, ouvrir, manger, dormir, être debout, s'asseoir, bouger, écouter, sonner parmi d'autres.
  - EXEMPLES:
{examples_0}
- CATÉGORIE 1
  - NOM: aggression
  - DÉFINITION: Action violente. Liée à des notions comme tuer, se battre, frapper, le suicide ou la menace.
  - EXEMPLES:
{examples_1}
- CATÉGORIE 2
  - NOM: aparte
  - DÉFINITION: Aparté (le personnage s'adresse au public ou est seul).
  - EXEMPLES:     
{examples_2}
- CATÉGORIE 3
  - NOM: delivery
  - DÉFINITION: Décrivent comment est interprétée une réplique, par exemple en ce qui concerne la voix ou l'expression vocale d'une émotion. Utilisée également lorsque le personnage chante. Peut se référer à des notions telles que le personnage montrant de la colère ou étant furieux, étant sérieux, heureux, hésitant, montrant de l'enthousiasme, de l'émotion, de l'emphase, se montrant gentil, faisant une grimace, montrant un sentiment, ou répétant une expression.
  - EXEMPLES: 
{examples_3}
- CATÉGORIE 4
  - NOM: entrance
  - DÉFINITION: Le personnage entre en scène.
  - EXEMPLES: 
{examples_4}
- CATÉGORIE 5
  - NOM: exit
  - DÉFINITION: Le personnage sort, quitte la scène.
  - EXEMPLES: 
{examples_5}
- CATÉGORIE 6
  - NOM: interaction
  - DÉFINITION: Interaction non verbale entre les personnages. L'interaction doit être non verbale, par exemple regarder, pointer du doigt, toucher, aider, tirer, pousser parmi d'autres types d'interactions non verbales.
  - EXEMPLES: 
{examples_6}
- CATÉGORIE 7
  - NOM: movement
  - DÉFINITION: Déplacement du personnage (mais pas une entrée ou sortie). Parfois lié à des notions comme s'approcher, s'éloigner, suivre un personnage, reculer.
  - EXEMPLES: 
{examples_7}
- CATÉGORIE 8
  - NOM: music
  - DÉFINITION: Noms des airs (dans les pièces de théâtre avec des chansons), ou description de la musique. Catégorie non utilisée lorsque la didascalie fait référence à un personnage qui chante. La didascalie commence souvent par le mot « AIR » ou « Air ». Si la didascalie commence par ces mots, il s'agit très probablement d'une didascalie de cette catégorie, et les mots suivants constituent le nom de l'air.
  - EXEMPLES: 
{examples_8}
- CATÉGORIE 9
  - NOM: narration
  - DÉFINITION: Didascalie longue, à caractère narratif, à destination des lecteurs. Généralement de longues didascalies. Elles peuvent relater une séquence d'actions des personnages. Elles peuvent également faire référence à des bruits ou à des phénomènes météorologiques.
  - EXEMPLES: 
{examples_9}
- CATÉGORIE 10
  - NOM: object
  - DÉFINITION: Décrit un objet ou l'interaction d'un personnage avec un objet, y compris donner ou recevoir un objet ou manipuler l'objet de quelque manière que ce soit, entre autres interactions. L'objet peut être des vêtements, des costumes. Quelques verbes liés à cette catégorie sont jeter, déchirer, obtenir, donner, habiller, laisser tomber, fermer parmi d'autres.
  - EXEMPLES: 
{examples_10}
- CATÉGORIE 11
  - NOM: setting
  - DÉFINITION: Description de la scène ou lieu de la pièce.
  - EXEMPLES: 
{examples_11}
- CATÉGORIE 12
  - NOM: toward
  - DÉFINITION: Indique le destinataire d'une réplique.
  - EXEMPLES: 
{examples_12}

"""