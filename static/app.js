const axios = require('axios');

const API_BASE_URL = 'http://localhost:5000/api';

// register a user
async function registerUser(email, password) {
    try {
        const response = await axios.post(`${API_BASE_URL}/users/register`, {
            email: email,
            password: password
        });
        console.log('Register Response:', response.data);
    } catch (error) {
        console.error('Register Error:', error.response.data);
    }
}

// login a user
async function loginUser(email, password) {
    try {
        const response = await axios.post(`${API_BASE_URL}/users/login`, {
            email: email,
            password: password
        });
        console.log('Login Response:', response.data);
        return response.data;
    } catch (error) {
        console.error('Login Error:', error.response.data);
    }
}

// fetch books
async function fetchBooks(authToken) {
    try {
        const response = await axios.get(`${API_BASE_URL}/books`, {
            headers: {
                Authorization: `Bearer ${authToken}`
            }
        });
        console.log('Books Response:', response.data);
    } catch (error) {
        console.error('Fetch Books Error:', error.response.data);
    }
}

async function testAPI() {
    await registerUser('user@example.com', 'password123');
    const loginData = await loginUser('user@example.com', 'password123');
    if (loginData && loginData.access_token) {
        await fetchBooks(loginData.access_token);
    }
}

testAPI();