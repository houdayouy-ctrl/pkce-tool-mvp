import requests

URL_USERS = "https://jsonplaceholder.typicode.com/users"
  
try:
    response = requests.get(URL_USERS)
    
    if response.ok:
        print("Requête réussie (Code 200 OK).\n")  
        
        users_list = response.json()
        print ("Liste des 3 premiers utilisateurs :")
        print("---------------------------------")
        
        for i, user in enumerate(users_list[0:3]):
            print(f"Utilisateur #{user['id']} :")
            print(f"  Nom: {user['name']}")
            print(f"  Email: {user['email']}")
            if i < 2:
                print("---")
                
                
            else:
        print(f"Erreur lors de la requête : Code {response.status_code}")
        
                except requests.exceptions.RequestException as e:
    # Gère les problèmes de connexion réseau ou DNS
    print(f"Erreur de connexion : {e}")
    
    
import requests

URL_POSTS = "https://jsonplaceholder.typicode.com/posts"

nouvel_article = { 
    "title": "Mon nouvel article de test",
    "body": "Ceci est un contenu de test.",
    "userId": 1 
}
try:
    response = requests.post(URL_POSTS, json=nouvel_article) #Fais une requête POST pour envoyer cet article à cette adress