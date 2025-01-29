import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/selectcustomer/';

export interface CustomerData {
  CustomerData: string; // Kombinasi CustomerID dan Name
  NPWP: string;
  Address: string;
  Phone: string;
  BankAccount: string;
}

/**
 * Fetch customer data from the API.
 * @param customerdata Optional parameter to filter by specific customer.
 * @returns List of customer data or a specific customer's details.
 */
export const fetchCustomerData = async (customerdata?: string): Promise<CustomerData[]> => {
  try {
    // Call the API with optional customerdata parameter
    const response = await axios.get(API_URL, {
      params: { customerdata: customerdata || '' }, // Send parameter if provided, or empty string
    });

    // Return customer data list from the API
    return response.data.customers; // Response matches the structure from the Python API
  } catch (error) {
    console.error('Error fetching customer data:', error);
    throw new Error('Failed to fetch customer data');
  }
};
