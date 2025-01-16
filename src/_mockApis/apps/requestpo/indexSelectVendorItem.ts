import axios from 'axios';

// URL endpoint API
const API_URL = 'http://127.0.0.1:8000/selectvendoritem/';

// Interface untuk struktur data item vendor
export interface VendorItem {
  VendorItemData: string; // Kombinasi VendorItemID dan ItemName
  ItemName: string;       // Nama barang
  Price: number;          // Harga barang
  Unit: string;           // Satuan barang
}

/**
 * Fungsi untuk mengambil data barang dari vendor yang dipilih.
 * @param vendordata Vendor data (misalnya: "VS0112 - Monster Inc.")
 * @returns Array berisi daftar barang vendor.
 */
export const fetchVendorItems = async (vendordata: string): Promise<VendorItem[]> => {
  if (!vendordata) {
    console.warn('Vendor data is empty. Fetching all items is not recommended.');
  }

  try {
    const response = await axios.get(API_URL, {
      params: { vendordata }, // Kirim parameter ke API
    });

    return response.data.vendor_items || [];
  } catch (error) {
    console.error('Error fetching vendor items:', error);
    throw new Error('Failed to fetch vendor items');
  }
};