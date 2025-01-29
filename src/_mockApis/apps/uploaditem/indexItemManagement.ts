import axios from 'axios';
import * as XLSX from 'xlsx'; // Library untuk membaca file Excel

export interface TableRow {
  ItemName: string;
  ItemQty: string;
  Notes: string;
  DateInOut: string;
  AddUser: string;
}

const API_BASE_URL = 'http://127.0.0.1:8000/itemmanagement/';

/**
 * Fungsi untuk membaca file Excel dan memprosesnya menjadi format string dengan separator `|`
 * @param file File Excel yang diunggah
 * @returns Promise dengan data terproses
 */
export const processExcelFile = async (file: File): Promise<{ itemName: string; itemQty: string; notes: string }> => {
  try {
    const data = await file.arrayBuffer();
    const workbook = XLSX.read(new Uint8Array(data), { type: 'array' });
    const sheetName = workbook.SheetNames[0];
    const sheet = workbook.Sheets[sheetName];
    const jsonData = XLSX.utils.sheet_to_json(sheet);

    // Validasi apakah kolom sesuai dengan template
    const requiredColumns = ['ItemName', 'ItemQty', 'Notes'];
    const firstRowKeys = Object.keys(jsonData[0] || {});
    const isValid = requiredColumns.every((col) => firstRowKeys.includes(col));
    if (!isValid) {
      throw new Error(`File tidak sesuai template. Kolom yang diperlukan: ${requiredColumns.join(', ')}`);
    }

    // Proses data menjadi string dengan separator `|`
    let itemName = '';
    let itemQty = '';
    let notes = '';

    jsonData.forEach((row: any, index: number) => {
      const name = row['ItemName'] || '';
      const qty = row['ItemQty'] || '';
      const note = row['Notes'] || '';

      if (!name || !qty) {
        throw new Error('Kolom ItemName dan ItemQty tidak boleh kosong.');
      }

      itemName += name + (index < jsonData.length - 1 ? '|' : '');
      itemQty += qty + (index < jsonData.length - 1 ? '|' : '');
      notes += note + (index < jsonData.length - 1 ? '|' : '');
    });

    return { itemName, itemQty, notes };
  } catch (error) {
    throw new Error(`Error processing Excel file: ${error}`);
  }
};

/**
 * Fungsi untuk memasukkan data ke tabel utama menggunakan stored procedure
 * @param category Kategori: BARANG MASUK atau BARANG KELUAR
 * @param date Tanggal: YYYY-MM-DD
 * @param itemName Gabungan ItemName dari file Excel
 * @param itemQty Gabungan ItemQty dari file Excel
 * @param notes Gabungan Notes dari file Excel
 */
export const insertData = async (
  category: string,
  date: string,
  itemName: string,
  itemQty: string,
  notes: string
): Promise<void> => {
  try {
    await axios.post(API_BASE_URL, {
      param_kategori: category,
      param_date: date,
      param_itemname: itemName,
      param_itemqty: itemQty,
      param_notes: notes,
    });
  } catch (error) {
    console.error('Error inserting data:', error);
    throw new Error('Gagal memasukkan data ke tabel utama.');
  }
};

/**
 * Fungsi untuk mengambil data dari tabel BARANG MASUK dan BARANG KELUAR
 * @returns Data dari kedua kategori
 */
export const fetchData = async (): Promise<{ [key: string]: TableRow[] }> => {
  try {
    const response = await axios.get(API_BASE_URL);
    return response.data;
  } catch (error) {
    console.error('Error fetching data:', error);
    throw new Error('Gagal mengambil data.');
  }
};

/**
 * Fungsi untuk mengunduh template Excel berdasarkan kategori
 * @param category Kategori: BARANG MASUK atau BARANG KELUAR
 */
export const downloadTemplate = async (category: string): Promise<void> => {
    if (!category) {
      throw new Error('Kategori harus dipilih.');
    }
  
    try {
      // Panggil endpoint backend untuk mengunduh template
      const response = await axios.get(`http://127.0.0.1:8000/itemmanagement/template/${category}/`, {
        responseType: 'blob', // Pastikan respons berupa file
      });
  
      // Buat URL untuk file Excel
      const blob = new Blob([response.data], {
        type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
      });
  
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `Template_${category}.xlsx`);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Error downloading template:', error);
      throw new Error('Gagal mengunduh template. Silakan coba lagi.');
    }
  };
  