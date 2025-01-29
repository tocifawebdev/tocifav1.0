import axios from 'axios';

// URL endpoint API
const API_URL = 'http://127.0.0.1:8000/selectcustomeritem/';

// Interface untuk struktur data item pelanggan
export interface CustomerItem {
  CustomerItemData: string; // Kombinasi CustomerItemID dan ItemName
  ItemName: string;         // Nama barang
  Unit: string;             // Satuan barang
}

/**
 * Fungsi untuk mengambil semua data barang pelanggan.
 * @returns Array berisi daftar barang pelanggan.
 */
export const fetchCustomerItems = async (): Promise<CustomerItem[]> => {
  try {
    // Panggil API untuk mengambil data barang pelanggan
    const response = await axios.get(API_URL);

    // Mengembalikan daftar barang pelanggan dari respons API
    return response.data.customer_items || [];
  } catch (error) {
    console.error('Error fetching customer items:', error);
    throw new Error('Failed to fetch customer items');
  }
};
