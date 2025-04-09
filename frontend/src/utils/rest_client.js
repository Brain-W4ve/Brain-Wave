import axios from "axios";

class ApiClient {
  constructor(baseURL) {
    this.baseURL = baseURL;
    this.token = localStorage.getItem("token") || null;

    this.axiosInstance = axios.create({
      baseURL: this.baseURL,
      headers: {
        "Content-Type": "application/json",
      },
    });

    this.axiosInstance.interceptors.request.use((config) => {
      if (this.token) {
        config.headers.Authorization = `Bearer ${this.token}`;
      }
      return config;
    });
  }

  setToken(token) {
    this.token = token;
    localStorage.setItem("token", token);
  
    this.axiosInstance.defaults.headers.common["Authorization"] = `Bearer ${token}`;
  }
  

  clearToken() {
    this.token = null;
    localStorage.removeItem("token");
  
    delete this.axiosInstance.defaults.headers.common["Authorization"];
  }

  async request(method, url, data = null, config = {}) {
    console.log("")
    try {
      const response = await this.axiosInstance.request({
        method,
        url,
        data,
        ...config,
      });
      return await response.data;
    } catch (error) {
      console.error("API Error:", error);
      throw error.response?.data || error;
    }
  }

  async login(email, password) {
    const data = { email, password };
    const response = await this.request("post", "/login", data);
    if (response.token) this.setToken(response.token);
    return response;
  }

  async register(userData) {
    const response = await this.request("post", "/register", userData);
    if (response.token) this.setToken(response.token);
    return response;
  }
}


export default new ApiClient(process.env.REACT_APP_API_URL || "http://localhost:5000");
