import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/selectvendor/';

export interface VendorData {
  VendorData: string; // Kombinasi VendorID dan Name
  Address: string;
  Phone: string;
  BankAccount: string;
}

/**
 * Fetch vendor data from the API.
 * @param vendordata Optional parameter to filter by specific vendor.
 * @returns List of vendor data or a specific vendor's details.
 */
export const fetchVendorData = async (vendordata?: string): Promise<VendorData[]> => {
  try {
    // Call the API with optional vendordata parameter
    const response = await axios.get(API_URL, {
      params: { vendordata: vendordata || '' }, // Kirim parameter jika ada, jika tidak kosongkan
    });

    // Return vendor data list from the API
    return response.data.vendors; // Response sesuai struktur dari Python API
  } catch (error) {
    console.error('Error fetching vendor data:', error);
    throw new Error('Failed to fetch vendor data');
  }
};
