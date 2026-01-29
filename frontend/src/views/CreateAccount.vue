<template>
  <div class="register">
    <h1>Create Account</h1>
    <form @submit.prevent="registerUser">
      <div>
        <label>Username:</label>
        <input type="text" v-model="username" required />
      </div>
      <div>
        <label>Full Name:</label>
        <input type="text" v-model="name" required />
      </div>
      <div>
        <label>Email:</label>
        <input type="email" v-model="email" required />
      </div>
      <div>
        <label>Password:</label>
        <input type="password" v-model="password" required />
      </div>
      <div>
        <label>Age:</label>
        <input type="number" v-model="age" />
      </div>
      <button type="submit" :disabled="loading">{{ loading ? 'Creating...' : 'Create Account' }}</button>
    </form>
    <p v-if="error" style="color:red">{{ error }}</p>
    <p v-if="success" style="color:green">{{ success }}</p>
    <router-link to="/login">Go to Login</router-link>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();
const username = ref('');
const name = ref('');
const email = ref('');
const password = ref('');
const age = ref('');
const error = ref('');
const success = ref('');
const loading = ref(false);

const API_BASE = 'http://127.0.0.1:5000/api';

const registerUser = async () => {
  error.value = '';
  success.value = '';
  loading.value = true;

  try {
    const response = await axios.post(`${API_BASE}/register`, {
      username: username.value,
      name: name.value,
      email: email.value,
      password: password.value,
      age: age.value ? parseInt(age.value) : null
    });

    success.value = response.data.message;
    console.log('User created:', response.data.user);

    // Redirect to login after 1s
    setTimeout(() => {
      router.push('/login');
    }, 1000);

  } catch (err) {
    if (err.response) {
      error.value = err.response.data.message;
    } else {
      error.value = 'Server error';
    }
    console.error(err);
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.register {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
}

.register div {
  margin-bottom: 15px;
}

button {
  padding: 8px 16px;
}
</style>
