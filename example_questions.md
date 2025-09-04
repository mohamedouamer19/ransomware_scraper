# Exemples de questions pour tester le workflow N8N Ransomware MCP

## 📊 ANALYSE DE MENACES

### Questions de base
- "Quels sont les groupes ransomware les plus actifs actuellement ?"
- "Montre-moi les statistiques générales des attaques ransomware"
- "Quels secteurs d'activité sont les plus ciblés ?"

### Questions sur les groupes spécifiques
- "Donne-moi des informations détaillées sur le groupe LockBit"
- "Quels sont les IOC (Indicateurs de Compromission) du groupe Conti ?"
- "Le groupe REvil est-il toujours actif ?"

## 🎯 INVESTIGATION D'INCIDENTS

### Recherche de victimes
- "Quelles entreprises françaises ont été victimes de ransomware ce trimestre ?"
- "Montre-moi les victimes récentes dans le secteur de la santé"
- "Y a-t-il eu des attaques contre des entreprises allemandes récemment ?"

### Analyse temporelle
- "Quelles sont les nouvelles victimes découvertes cette semaine ?"
- "Évolution des attaques au cours des 6 derniers mois"
- "Tendances des attaques par mois en 2024"

## 🔍 RECHERCHE D'IOC

### Par type d'indicateur
- "Liste des domaines malveillants utilisés par les ransomware"
- "Adresses IP associées aux attaques de ransomware"
- "Hashes de fichiers malveillants récents"

### Par groupe
- "Domaines utilisés par le groupe Akira"
- "Adresses IP du groupe LockBit"
- "Hashes de ransomwares du groupe Conti"

## 💬 NÉGOCIATIONS ET COMMUNICATIONS

### Analyse des négociations
- "Quelles négociations de rançon sont en cours ?"
- "Montre-moi les chats de négociation du groupe LockBit"
- "Détails de la négociation avec l'ID chat_123"

## 📰 CONTENU MÉDIATIQUE

### Communiqués de presse
- "Quels sont les derniers communiqués de presse sur les attaques ransomware ?"
- "Communiqués de presse français sur les cyberattaques"
- "Évolution des communiqués de presse en 2024"

### Notes de rançon
- "Quels groupes publient des notes de rançon ?"
- "Contenu de la note de rançon du groupe LockBit"
- "Liste des notes de rançon disponibles pour le groupe Conti"

## 🏢 ANALYSE SECTORIELLE

### Par secteur
- "Quels sont les secteurs les plus touchés par les ransomware ?"
- "Attaques contre les hôpitaux cette année"
- "Impact des ransomware sur le secteur bancaire"

### Par pays
- "Victimes françaises de ransomware"
- "Attaques aux États-Unis par secteur"
- "Comparaison des attaques France vs Allemagne"

## 🔧 OUTILS TECHNIQUES

### Règles YARA
- "Quels groupes ont des règles YARA disponibles ?"
- "Règles YARA pour détecter les malwares du groupe LockBit"

### Données CSIRT
- "Informations CSIRT pour la France"
- "Données de réponse aux incidents en Allemagne"

## 📈 ANALYSES AVANCÉES

### Tendances et statistiques
- "Évolution mensuelle des attaques en 2024"
- "Groupes les plus prolifiques cette année"
- "Analyse comparative des méthodes de chiffrement"

### Recherche flexible
- "Entreprises tech victimes de Conti"
- "Attaques contre l'éducation en Europe"
- "Victimes gouvernementales de ransomware"

## ⚡ QUESTIONS RAPIDES (pour les tests)

### Tests de base
- "Liste des groupes actifs"
- "Nombre total de victimes"
- "Dernières attaques découvertes"

### Tests d'IOC
- "Domaines malveillants récents"
- "IP suspectes"
- "Hashes de ransomware"

### Tests de fonctionnalités
- "Validation de l'API"
- "Test de connectivité"
- "Vérification des outils disponibles"

## 🎯 SCÉNARIOS D'USAGE RÉELS

### Pour un analyste de sécurité
1. "Quels sont les IOC du groupe le plus actif cette semaine ?"
2. "Victimes dans mon secteur d'activité ce mois-ci"
3. "Tendances des attaques contre les entreprises similaires à la mienne"

### Pour un incident response
1. "Toutes les victimes du groupe X cette année"
2. "IOC associés à cette attaque spécifique"
3. "Historique des négociations similaires"

### Pour la veille stratégique
1. "Évolution des attaques par pays"
2. "Nouveaux groupes apparus récemment"
3. "Changement dans les méthodes des groupes établis"

---

## 💡 CONSEILS POUR LES TESTS

1. **Commencez simple** : Testez d'abord les questions de base
2. **Vérifiez la connectivité** : Assurez-vous que le serveur MCP fonctionne
3. **Testez les filtres** : Utilisez les paramètres de filtrage pour limiter les résultats
4. **Vérifiez les erreurs** : Les erreurs API sont normales, elles indiquent des problèmes de configuration
5. **Soyez patient** : Les premières requêtes peuvent être lentes

## 🔧 DÉPANNAGE

Si une question ne fonctionne pas :
- Vérifiez la syntaxe de la question
- Assurez-vous que l'outil demandé existe
- Contrôlez les paramètres requis
- Vérifiez la connectivité réseau

Les réponses peuvent varier selon :
- La disponibilité de l'API ransomware.live
- Les données disponibles dans la base
- Les limitations de l'API key
