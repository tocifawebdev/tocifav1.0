import axios from 'axios';

export const fetchDropdownKategori = async (): Promise<string[]> => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/listkategori/');
    return response.data.map((kategori: { Category: string }) => kategori.Category);
  } catch (error) {
    throw new Error('Gagal mengambil kategori dropdown.');
  }
};
