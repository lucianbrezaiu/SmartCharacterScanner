"Smart Character Scanner" este o aplicație web de tip client-server ce oferă utilizatorului posibilitatea de a obține varianta editabilă 
a unui text de tipar dintr-o poză. Aplicația preia imaginea încărcată de utilizator, o segmentează în cuvinte și litere care urmează să
fie recunoscute și va compune textul final care va fi returnat. Utilizatorul va putea salva rezultatul recunoscut în documente de format
pdf. Structura:

-> client - reprezintă componenta client a aplicației realizată în Vue.js. Pentru a porni clientul, intru in folderul client, deschid o
consolă și rulez: 

npm run serve

-> server - reprezintă componenta server a aplicației realizată în Flask și Python. Aplicația trebuie să aibă următoarele fișiere:
	\1. din dllFactory are nevoie de ./build/bin/Debug/imageProcessingd.dll
	\2. din neuralNetwork are nevoie ./model.json și ./weights.h5
	
	Pentru a porni serverul, intru in folderul server, deschid o consolă și rulez:

.\env\Scripts\activate
python server.py