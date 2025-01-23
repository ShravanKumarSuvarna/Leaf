import { initializeApp } from 'https://www.gstatic.com/firebasejs/9.16.0/firebase-app.js';
import { getAuth } from 'https://www.gstatic.com/firebasejs/9.16.0/firebase-auth.js';

const firebaseConfig = {
  apiKey: 'AIzaSyAd5Y_nccZadhEbXd04zcaFwEuTEi-areQ',
  authDomain: 'leaf-72ae9.firebaseapp.com',
  projectId: 'leaf-72ae9',
  storageBucket: 'leaf-72ae9.appspot.com',
  messagingSenderId: '874769964624',
  appId: '1:874769964624:web:c30b3a84d7fc52cf717b55',
  measurementId: 'G-2N6JWSZ6BX',
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
