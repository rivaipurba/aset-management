import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/',
  headers: { 'Content-Type': 'application/json' },
  timeout: 10000,
});

function setAuthToken(token) {
  if (token) apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  else delete apiClient.defaults.headers.common['Authorization'];
}

// optional: intercept response errors to attach server message
apiClient.interceptors.response.use(
  res => res,
  err => {
    // attach server message if possible
    if (err.response?.data) {
      err.serverMessage = err.response.data;
    }
    return Promise.reject(err);
  }
);

export default {
  apiClient,
  setAuthToken,
  login(creds) { return apiClient.post('auth/token/', creds); },
  refresh(refreshToken) { return apiClient.post('auth/token/refresh/', { refresh: refreshToken }); },

  listAssets(params) { return apiClient.get('assets/', { params }); },
  getAsset(id) { return apiClient.get(`assets/${id}/`); },
  createAsset(payload) { return apiClient.post('assets/', payload); },
  updateAsset(id, payload) { return apiClient.patch(`assets/${id}/`, payload); },
  deleteAsset(id) { return apiClient.delete(`assets/${id}/`); },
  moveAsset(id, payload) { return apiClient.post(`assets/${id}/move/`, payload); },

  listMovements(params) { return apiClient.get('movements/', { params }); },
};
