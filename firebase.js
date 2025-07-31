// src/firebase.js
const { initializeApp } = require("firebase/app");
const { getFirestore } = require("firebase/firestore");

const firebaseConfig = {
  apiKey: "AIzaSyAmCvZANP7wxR1JcUxka08Q7ZGTGTi4cTc",
  authDomain: "t-flow-ai.firebaseapp.com",
  projectId: "t-flow-ai",
  storageBucket: "t-flow-ai.firebasestorage.app",
  messagingSenderId: "16667065969",
  appId: "1:16667065969:web:509fb8fa968326ddb6a5d0",
  measurementId: "G-TVGPVGZRYK"
};

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

module.exports = { db };
