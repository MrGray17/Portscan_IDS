# Guide d'Entretien — Analyse des Vulnérabilités Réseaux
## IA & Automatisation de la Détection d'Intrusions
### Projet Académique

| Champ | Détail |
|---|---|
| Module | IA |
| Statut | Projet Académique |
| Étudiant 1 | El Kartouti Anas |
| Étudiant 2 | Lekhbioui Adil |
| Étudiant 3 | Moulay Anas |
| Étudiant 4 | Hammoubel El Yazid |
| Étudiant 5 | Nafia Khadija |

---

## 1. Phase d'Introduction (Mise en situation)

**Q1.1 :** « Pourriez-vous vous présenter brièvement et décrire votre rôle ainsi que le type d'architecture réseau (LAN, Cloud, réseaux hybrides) que vous gérez ou utilisez au quotidien ? »

**Q1.2 :** « De manière générale, quels sont les défis ou les incidents majeurs auxquels vous êtes le plus fréquemment confronté pour garantir la disponibilité et la sécurité de cette infrastructure ? »

---

## 2. Phase de Développement (Exploration du problème cible)

**Q2.1 :** « Pourriez-vous me décrire en détail une expérience récente où vous avez constaté un comportement suspect, une anomalie de trafic ou une baisse de performance inexpliquée sur le réseau ? »

**Q2.2 :** « Selon votre expérience, lorsque le réseau subit ce type de perturbations de manière furtive, quelles en sont les causes les plus courantes ? »

**Q2.3 :** « Face à ces anomalies, comment faites-vous la différence entre une simple panne de composant, une inondation de trafic malveillante (DDoS/surcharge), ou une infection par un malware interne ? »

**Q2.4 :** « Les attaquants procèdent souvent par des phases de reconnaissance avant de frapper. Comment percevez-vous ou détectez-vous ces tentatives de cartographie silencieuse (comme l'exploration de vos services ou les scans de ports) sur votre périmètre ? »

---

## 3. Phase d'Approfondissement (Limites actuelles et transition vers l'innovation)

**Q3.1 :** « Actuellement, quelles procédures, logs ou outils mobilisez-vous pour isoler la cause d'une intrusion ou d'un scan, et comment procédez-vous pour bloquer la menace ? »

**Q3.2 :** « Quelles sont les limites techniques ou humaines que vous rencontrez avec ces méthodes actuelles (temps de réaction, faux positifs, charge de travail) ? »

**Q3.3 :** « Face à la complexité des attaques, que penseriez-vous de l'intégration d'un modèle d'Intelligence Artificielle capable d'analyser le trafic en temps réel pour détecter de manière autonome ces comportements suspects ? »

**Q3.4 :** « Pensez-vous qu'un modèle IA serait pertinent non seulement pour détecter, mais aussi pour intervenir directement sur l'infrastructure (ex : bloquer une IP, modifier dynamiquement l'accès) pour vous faire gagner du temps ? »

---

## 4. Phase de Conclusion (Critères d'acceptabilité de la solution)

**Q4.1 :** « Pour qu'une solution basée sur l'IA vous soit réellement utile, quelles devraient être ses caractéristiques principales (ex : type de tableau de bord, alertes en temps réel, visibilité du réseau) ? »

**Q4.2 :** « Quelles seraient vos exigences strictes ou vos craintes (ex : confidentialité des flux, blocage accidentel d'un trafic légitime) avant d'autoriser une IA à interagir avec vos routeurs/pare-feux ? »

**Q4.3 :** « En résumé, si ce système intelligent et autonome, garantissant un faible taux d'erreur, était déployé sur votre infrastructure, seriez-vous prêt à l'adopter dans vos opérations quotidiennes ? »

---
---

# Entretien 1 — Ouzizi Amine
*(Étudiant en 2ème année cycle ingénieur, Réseaux & Télécommunications, option Sécurité)*

---

**Q1.1 :** Pourriez-vous vous présenter brièvement et décrire votre rôle ainsi que le type d'architecture réseau que vous gérez ou utilisez au quotidien ?

**R1.1 :** Je m'appelle Ouzizi Amine, je suis étudiant en deuxième année du cycle ingénieur en réseaux et systèmes de télécommunication, option sécurité des réseaux et des systèmes d'information. J'utilise le réseau Wi-Fi de l'école tous les jours et je fais souvent tourner des environnements de test locaux sur mon poste Windows/Ubuntu pour avancer sur mes projets académiques et professionnels.

---

**Q1.2 :** De manière générale, quels sont les défis ou les incidents majeurs auxquels vous êtes le plus fréquemment confronté pour garantir la disponibilité de cette infrastructure ?

**R1.2 :** Le grand défi pour moi, c'est que la connexion lâche souvent au milieu d'une session de travail sans explication, ou que mes ports locaux deviennent soudainement inaccessibles depuis les autres machines de mon groupe de TP.

---

**Q2.1 :** Pourriez-vous me décrire en détail une expérience récente où vous avez constaté un comportement suspect, une anomalie de trafic ou une baisse de performance inexpliquée ?

**R2.1 :** La semaine dernière, mon serveur web local plantait en boucle. J'ai regardé les logs de mon système et j'ai vu des centaines de requêtes incomplètes sur différents ports, venant d'adresses IP appartenant au réseau étudiant.

---

**Q2.2 :** Selon votre expérience, lorsque le réseau subit ce type de perturbations de manière furtive, quelles en sont les causes les plus courantes ?

**R2.2 :** Souvent, ce sont des scripts automatisés ou des malwares installés à l'insu d'un autre étudiant sur son PC, qui essaient de trouver d'autres machines vulnérables sur le réseau local.

---

**Q2.3 :** Face à ces anomalies, comment faites-vous la différence entre une simple panne de composant, une inondation de trafic malveillante ou une infection ?

**R2.3 :** C'est simple : je regarde les outils de monitoring de mon poste. Si l'utilisation CPU est normale mais que mes ports de communication sautent les uns après les autres, je sais que la perturbation vient de l'extérieur.

---

**Q2.4 :** Les attaquants procèdent souvent par des phases de reconnaissance. Comment percevez-vous ces tentatives de cartographie silencieuse sur votre périmètre ?

**R2.4 :** Sur mon système, je le vois si je prends le temps de vérifier les journaux de mon pare-feu local. Mais c'est difficile de vérifier ça manuellement tout le temps.

---

**Q3.1 :** Actuellement, quelles procédures, logs ou outils mobilisez-vous pour isoler la cause et comment procédez-vous pour bloquer la menace ?

**R3.1 :** Je regarde les connexions actives dans mon terminal et j'ajoute l'IP suspecte manuellement dans les règles de rejet de mon pare-feu.

---

**Q3.2 :** Quelles sont les limites techniques ou humaines que vous rencontrez avec ces méthodes actuelles ?

**R3.2 :** Ça demande d'avoir littéralement les yeux tout le temps sur un moniteur de trafic. Je ne peux pas avancer sur mon code et surveiller le réseau en même temps — c'est une perte de temps.

---

**Q3.3 :** Face à la complexité des attaques, que penseriez-vous de l'intégration d'un modèle d'Intelligence Artificielle capable d'analyser le trafic en temps réel pour détecter ces comportements ?

**R3.3 :** Ce serait génial bien sûr. L'IA pourrait comprendre mon comportement habituel de développeur sur le réseau et bloquer uniquement ce qui est vraiment un trafic de reconnaissance malveillant.

---

**Q3.4 :** Pensez-vous qu'un modèle IA serait pertinent non seulement pour détecter, mais aussi pour intervenir directement sur l'infrastructure (ex : bloquer une IP, modifier dynamiquement l'accès) ?

**R3.4 :** Oui, surtout la modification dynamique — si l'IA change le port de mon serveur de test dès qu'il est ciblé par un scan, ça me protège sans couper la connexion avec mes collègues de TP.

---

**Q4.1 :** Pour qu'une solution basée sur l'IA vous soit réellement utile, quelles devraient être ses caractéristiques principales ?

**R4.1 :** J'aimerais un tableau de bord web très léger qui me montre simplement quels sont mes ports actuellement visés par des requêtes externes et le niveau de menace global.

---

**Q4.2 :** Quelles seraient vos exigences strictes ou vos craintes avant d'autoriser une IA à interagir avec le réseau ?

**R4.2 :** Ma crainte principale est que ce modèle d'IA ralentisse les performances de ma propre machine s'il consomme trop de ressources processeur pour analyser les flux en continu.

---

**Q4.3 :** En résumé, si ce système intelligent et autonome garantissant un faible taux d'erreur était déployé, seriez-vous prêt à l'adopter ?

**R4.3 :** Sans aucune hésitation — cela sécuriserait mes projets locaux sans aucun effort de ma part.

---
---

# Entretien 2 — Fahd
*(Étudiant en 1ère année cycle ingénieur, Informatique)*

---

**Q1.1 :** Pourriez-vous vous présenter brièvement et décrire votre rôle ainsi que le type d'architecture réseau que vous gérez ou utilisez au quotidien ?

**R1.1 :** Je m'appelle Fahd. Je suis étudiant en 1ère année du cycle ingénieur en informatique. Je me connecte au réseau de l'école avec mon PC personnel pour suivre les cours et faire des travaux pratiques qui demandent souvent des communications multi-ports avec des machines virtuelles.

---

**Q1.2 :** De manière générale, quels sont les défis ou les incidents majeurs auxquels vous êtes le plus fréquemment confronté pour garantir la disponibilité de cette infrastructure ?

**R1.2 :** Ce sont les déconnexions intempestives. Parfois, le réseau me jette simplement parce que je lance un outil de diagnostic nécessaire pour un projet. Le filtrage est très restrictif.

---

**Q2.1 :** Pourriez-vous me décrire en détail une expérience récente où vous avez constaté un comportement suspect, une anomalie de trafic ou une baisse de performance inexpliquée ?

**R2.1 :** Récemment, je lançais un script de test réseau totalement inoffensif vers une machine virtuelle, et d'un coup, impossible de charger la moindre page web. Mon adresse IP avait été mise sur liste noire par la passerelle de l'école.

---

**Q2.2 :** Selon votre expérience, lorsque le réseau subit ce type de perturbations de manière furtive, quelles en sont les causes les plus courantes ?

**R2.2 :** Je pense que ce sont des règles de sécurité beaucoup trop rigides qui s'activent pour un rien. Dès qu'on sort du trafic web standard, le système panique.

---

**Q2.3 :** Face à ces anomalies, comment faites-vous la différence entre une simple panne de composant, une inondation de trafic malveillante ou une infection ?

**R2.3 :** C'est difficile à dire. En général, je fais un ping vers la passerelle : si elle répond mais que tout le reste est bloqué, je sais que j'ai été filtré arbitrairement par le système de détection d'intrusion.

---

**Q2.4 :** Les attaquants procèdent souvent par des phases de reconnaissance. Comment percevez-vous ces tentatives de cartographie silencieuse sur votre périmètre ?

**R2.4 :** En tant qu'utilisateur, je ne les détecte pas du tout. Je subis juste les conséquences quand l'administrateur réseau décide de bloquer des segments entiers par précaution parce qu'il a vu un scan.

---

**Q3.1 :** Actuellement, quelles procédures, logs ou outils mobilisez-vous pour isoler la cause et comment procédez-vous pour bloquer la menace ?

**R3.1 :** Je n'ai pas les droits d'administration sur le matériel de l'école, donc je ne peux rien faire à part redémarrer ma machine ou changer de connexion en espérant que le blocage soit levé.

---

**Q3.2 :** Quelles sont les limites techniques ou humaines que vous rencontrez avec ces méthodes actuelles ?

**R3.2 :** Les faux positifs bien sûr ! Les règles actuelles ne comprennent absolument pas le contexte académique de mes requêtes et me bloquent sans raison valable. C'est vraiment insupportable quand on essaie de travailler.

---

**Q3.3 :** Face à la complexité des attaques, que penseriez-vous de l'intégration d'un modèle d'Intelligence Artificielle capable d'analyser le trafic en temps réel pour détecter ces comportements ?

**R3.3 :** Si l'IA est correctement entraînée et qu'elle réduit drastiquement les faux positifs en différenciant un vrai scan d'un TP étudiant, je suis à 100 % pour.

---

**Q3.4 :** Pensez-vous qu'un modèle IA serait pertinent non seulement pour détecter, mais aussi pour intervenir directement sur l'infrastructure (ex : bloquer une IP, modifier dynamiquement l'accès) ?

**R3.4 :** Bloquer une IP automatiquement, oui, à condition qu'on puisse facilement contester le blocage si c'est une erreur. L'idée de modifier les accès dynamiquement me semble très intelligente pour esquiver l'attaquant sans tout couper.

---

**Q4.1 :** Pour qu'une solution basée sur l'IA vous soit réellement utile, quelles devraient être ses caractéristiques principales ?

**R4.1 :** Il faut avant tout de la transparence. Si mon flux est bloqué, je veux une notification claire qui m'explique exactement quelle caractéristique de mon trafic a poussé l'IA à prendre cette décision.

---

**Q4.2 :** Quelles seraient vos exigences strictes ou vos craintes avant d'autoriser une IA à interagir avec le réseau ?

**R4.2 :** Le taux de faux positifs doit être très faible. Je ne veux plus être empêché de rendre un projet à cause d'une règle de sécurité mal calibrée.

---

**Q4.3 :** En résumé, si ce système intelligent et autonome garantissant un faible taux d'erreur était déployé, seriez-vous prêt à l'adopter ?

**R4.3 :** Si ça met fin aux blocages abusifs que l'on subit actuellement, je serais le premier à plaider pour son installation.

---
---

# Entretien 3 — Étudiante en Génie des Réseaux & Télécommunications (Cybersécurité)

---

## 1. Phase d'Introduction (Mise en situation)

**Q1.1 :** Je suis étudiante en génie des réseaux et télécommunications, spécialisée en cybersécurité. Dans le cadre de mes travaux pratiques, je travaille sur des architectures LAN segmentées, des environnements cloud et hybrides. Une grande partie de mes travaux porte spécifiquement sur la sécurité périmétrique et la surveillance du trafic entrant — notamment la détection de comportements de reconnaissance réseau comme les portscans.

**Q1.2 :** Le défi le plus critique que j'identifie est la détection précoce des phases de reconnaissance. Avant toute attaque, un attaquant effectue obligatoirement un scan de ports pour cartographier l'infrastructure cible. Or, ces scans — surtout lorsqu'ils sont réalisés à faible cadence — passent souvent inaperçus dans les systèmes de surveillance traditionnels, ce qui en fait une menace sournoise et sous-estimée.

---

## 2. Phase de Développement (Exploration du problème cible)

**Q2.1 :** Lors d'un TP, j'ai observé sur Wireshark un flux de paquets SYN provenant d'une même source, ciblant séquentiellement des ports différents d'un hôte — signature classique d'un SYN scan (Nmap -sS). Ce comportement était suffisamment lent pour ne pas déclencher les seuils d'alerte du pare-feu, mais clairement visible à l'analyse manuelle des captures réseau. C'est exactement ce type de menace furtive que je cherche à détecter de manière automatisée.

**Q2.2 :** Les causes les plus courantes de ces perturbations furtives sont précisément les techniques de scan avancées :

- **SYN scan (half-open)** — ne complète pas le handshake TCP pour éviter les logs
- **Scan à faible débit (slow scan)** — étale les requêtes sur plusieurs heures pour passer sous les seuils
- **Scan fragmenté** — découpe les paquets pour tromper les IDS
- **Scan distribué** — utilise plusieurs sources IP pour diluer la signature

**Q2.3 :** La différence entre un portscan et un incident classique se fait sur l'analyse des patterns de trafic :

- Un portscan génère des tentatives de connexion vers de nombreux ports distincts sur une même IP cible, avec un taux élevé de RST ou ICMP port unreachable en retour
- Une panne produit une interruption franche et localisée, sans ce schéma de balayage
- Un DDoS sature un seul service, contrairement au scan qui sonde méthodiquement l'ensemble des ports

L'utilisation de Snort, Suricata ou d'un SIEM permet de corréler ces événements et de distinguer ces cas automatiquement.

**Q2.4 :** Le portscan est lui-même la phase de reconnaissance. J'ai étudié en détail comment des outils comme Nmap, Masscan ou Zmap permettent à un attaquant de :

- Identifier les ports ouverts et les services exposés
- Déduire le système d'exploitation
- Cartographier la topologie réseau avant de planifier l'attaque

Ces tentatives laissent des traces dans les logs de pare-feux, mais leur détection fiable nécessite une analyse comportementale automatisée plutôt qu'une simple règle de seuil.

---

## 3. Phase d'Approfondissement (Limites actuelles et transition vers l'innovation)

**Q3.1 :** Face à un portscan détecté ou suspecté, la procédure que j'applique est :

- Capturer le trafic via tcpdump/Wireshark et analyser les patterns de connexion
- Consulter les logs du pare-feu pour identifier les tentatives de connexion refusées sur plusieurs ports
- Identifier la source (IP, géolocalisation, réputation via VirusTotal ou AbuseIPDB)
- Créer une règle de blocage dynamique sur le pare-feu ou l'IDS (Snort/Suricata)
- Documenter l'incident et surveiller si l'attaquant change de vecteur

**Q3.2 :** Les limites actuelles face aux portscans sont précisément ce qui motive mon intérêt pour l'IA :

- **Seuils fixes inefficaces :** un slow scan à 1 paquet/minute passe sous tous les radars classiques
- **Faux positifs élevés :** des outils légitimes (monitoring, scanners de vulnérabilités internes) génèrent des alertes inutiles
- **Pas de corrélation temporelle :** les IDS classiques ne relient pas des scans fragmentés sur plusieurs heures venant de la même source
- **Réaction manuelle trop lente :** le temps qu'un analyste identifie le scan, la phase de reconnaissance est souvent terminée

**Q3.3 :** C'est exactement là qu'un modèle d'IA apporte une valeur ajoutée décisive. Un modèle entraîné sur des features réseau (nombre de ports distincts contactés, ratio SYN/SYN-ACK, intervalles entre paquets, distribution des ports cibles) peut :

- Détecter des scans lents et fragmentés invisibles aux IDS classiques
- Distinguer un scan malveillant d'un outil de monitoring légitime
- Corréler des événements sur de longues fenêtres temporelles
- Générer des alertes contextualisées et priorisées plutôt qu'un simple log brut

Des approches comme les Random Forests, LSTM ou autoencoders ont montré des résultats très prometteurs sur des datasets comme KDD Cup 99 ou CICIDS2017 pour cette problématique précise.

**Q3.4 :** Oui, et c'est même l'étape logique suivante. Une fois le portscan détecté avec un haut niveau de confiance, l'IA devrait pouvoir :

- Bloquer automatiquement l'IP source via une règle dynamique sur le pare-feu
- Augmenter le niveau de surveillance sur le segment réseau ciblé
- Alerter en temps réel l'équipe SOC avec un rapport structuré de l'incident

Cela transforme la détection passive en une réponse active et autonome, réduisant drastiquement la fenêtre d'exposition.

---

## 4. Phase de Conclusion (Critères d'acceptabilité de la solution)

**Q4.1 :** Pour une solution IA dédiée à la détection de portscans, les caractéristiques essentielles seraient :

- Analyse en temps réel des flux réseau avec détection comportementale (pas uniquement par signatures)
- Tableau de bord visualisant les tentatives de scan, les ports ciblés et la chronologie des événements
- Scoring de dangerosité pour prioriser les alertes selon le profil du scan (type, cadence, ports ciblés)
- Corrélation temporelle capable de relier des événements fragmentés sur de longues périodes

**Q4.2 :** Mes exigences strictes porteraient sur :

- **Taux de faux positifs maîtrisé** — un blocage abusif d'un outil de monitoring interne peut paralyser l'infrastructure
- **Explicabilité des décisions** — je dois comprendre pourquoi le modèle a classifié un trafic comme scan malveillant
- **Résistance à l'évasion** — le modèle doit rester robuste face aux techniques de scan avancées conçues pour le tromper
- **Confidentialité des flux analysés** — les données réseau contiennent des informations sensibles qui ne doivent pas quitter l'infrastructure

**Q4.3 :** Absolument. La détection de portscans est un problème concret, bien délimité, et pour lequel l'IA apporte une réponse supérieure aux méthodes traditionnelles. Si le modèle démontre une haute précision de détection, une faible latence de réponse et une capacité d'adaptation aux nouvelles techniques de scan, je l'adopterais sans hésitation — et ce serait précisément le type de solution sur laquelle je souhaite travailler dans ma carrière en cybersécurité.

---
---

# Entretien 4 — Étudiant(e) en Informatique (2ème année)

---

**Q1.1 :** Pourriez-vous vous présenter brièvement et décrire votre rôle ainsi que le type d'architecture réseau que vous gérez ou utilisez au quotidien ?

**R1.1 :** Je m'appelle [Prénom]. Je suis étudiant en deuxième année informatique. Au quotidien, j'utilise principalement le réseau Wi-Fi de l'école pour accéder aux plateformes pédagogiques, faire des recherches, travailler sur GitHub et communiquer avec mon groupe de projet. En dehors des cours, j'utilise aussi parfois un petit environnement local avec Linux, Docker ou des machines virtuelles pour tester des applications web ou des scripts réseau. Donc je ne gère pas une architecture réseau professionnelle.

---

**Q1.2 :** De manière générale, quels sont les défis ou les incidents majeurs auxquels vous êtes le plus fréquemment confronté pour garantir la disponibilité de cette infrastructure ?

**R1.2 :** Le problème principal, c'est la disponibilité et la stabilité du réseau. À certaines heures, surtout quand beaucoup d'étudiants sont connectés, la connexion devient très lente. Parfois, le signal Wi-Fi est bon, mais les pages ne chargent pas ou les plateformes pédagogiques répondent très lentement. On peut aussi avoir des coupures temporaires, des pertes de paquets ou une latence élevée.

---

**Q2.1 :** Pourriez-vous me décrire en détail une expérience récente où vous avez constaté un comportement suspect, une anomalie de trafic ou une baisse de performance inexpliquée ?

**R2.1 :** Récemment, pendant un travail de groupe, on devait envoyer un fichier et accéder à une plateforme en ligne, mais la connexion était très lente. Le Wi-Fi était connecté, mais les requêtes mettaient beaucoup de temps à répondre, jusqu'à provoquer des erreurs de type time-out. J'ai essayé de tester avec d'autres sites et le problème semblait général. Ce qui était étrange, c'est que certains services fonctionnaient encore, mais très lentement, comme s'il y avait une saturation ou une anomalie dans le trafic réseau.

---

**Q2.2 :** Selon votre expérience, lorsque le réseau subit ce type de perturbations de manière furtive, quelles en sont les causes les plus courantes ?

**R2.2 :** D'après moi, il peut y avoir plusieurs causes. La première, c'est simplement la surcharge du réseau lorsque beaucoup d'utilisateurs sont connectés. Mais il peut aussi y avoir des machines qui génèrent trop de trafic, par exemple à cause de téléchargements lourds, de mises à jour automatiques ou même d'un malware. Dans un contexte plus sécurité, une machine compromise pourrait lancer des scans de ports, envoyer beaucoup de requêtes ou tenter de découvrir les services ouverts sur le réseau. Ce type d'activité peut être discret au début, mais il peut quand même dégrader les performances.

---

**Q2.3 :** Face à ces anomalies, comment faites-vous la différence entre une simple panne de composant, une inondation de trafic malveillante ou une infection ?

**R2.3 :** À mon niveau, je ne peux pas le confirmer avec certitude, parce que je n'ai pas accès aux logs des routeurs ou des pare-feux. Mais je peux faire quelques vérifications simples. Par exemple, je teste si le problème concerne seulement mon poste ou plusieurs étudiants. Je peux aussi faire un ping vers une passerelle ou vers un site externe pour voir la latence et les pertes de paquets. Si mon ordinateur est le seul impacté, je vérifie les processus qui consomment le réseau ou je lance un scan antivirus.

---

**Q3.1 :** Actuellement, quelles procédures, logs ou outils mobilisez-vous pour isoler la cause et comment procédez-vous pour bloquer la menace ?

**R3.1 :** Personnellement, je commence par des tests simples : vérifier la connexion, faire un ping, tester un autre navigateur ou un autre appareil, puis regarder si une application consomme beaucoup de bande passante. Dans mes projets personnels, je peux utiliser des outils comme Wireshark ou netstat pour observer les connexions actives, mais dans le réseau de l'école je n'ai pas les droits nécessaires pour analyser toute l'infrastructure. Pour bloquer une menace, je ne peux pas agir directement sur le réseau. Je peux seulement sécuriser ma propre machine, fermer des applications suspectes, lancer un antivirus ou signaler le problème au service informatique.

---

**Q3.3 :** Face à la complexité des attaques, que penseriez-vous de l'intégration d'un modèle d'Intelligence Artificielle capable d'analyser le trafic en temps réel pour détecter ces comportements ?

**R3.3 :** Je pense que c'est pertinent, parce qu'un modèle d'Intelligence Artificielle pourrait analyser des volumes de données beaucoup plus importants qu'un humain. Par exemple, il pourrait détecter des patterns anormaux comme un nombre inhabituel de connexions, des scans de ports, des tentatives répétées vers plusieurs services ou une hausse brutale de trafic. L'avantage, c'est qu'il pourrait réagir rapidement, surtout si le modèle est entraîné sur des comportements normaux et malveillants. Par contre, il faut que le modèle soit bien évalué pour éviter trop de faux positifs.

---

**Question complémentaire :** Si on développe une IA pour résoudre ce type de problème, seriez-vous prêt à l'utiliser ? Si oui, quelles fonctionnalités vous sembleraient essentielles et quelles seraient vos principales craintes ?

**Réponse :** Oui, je serais prêt à l'utiliser si elle améliore la stabilité du réseau et permet une détection rapide des anomalies. Les fonctionnalités importantes seraient une analyse en temps réel, des alertes claires et un tableau de bord simple. En revanche, mes principales craintes concernent la confidentialité des données, le risque de faux positifs et le fait que l'IA prenne des décisions automatiques sans contrôle humain.
