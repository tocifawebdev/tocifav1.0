import axios from 'axios';

// URL API untuk mendapatkan datetime
const DATETIME_API_URL = 'http://127.0.0.1:8000/datetime/';

// Fetch current date and time
export const fetchCurrentDateTime = async (): Promise<string> => {
  try {
    const response = await axios.get(DATETIME_API_URL);
    if (response.data && response.data.CurrentDateTime) {
      return response.data.CurrentDateTime;
    }
    throw new Error('Invalid response from server');
  } catch (error) {
    console.error('Error fetching current date and time:', error);
    throw new Error('Failed to fetch current date and time');
  }
};