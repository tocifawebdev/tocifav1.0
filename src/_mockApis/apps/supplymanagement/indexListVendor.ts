import axios from 'axios';

export type Vendor = {
    VendorData: string; // Sesuaikan nama properti dengan respons dari backend
};

export const fetchDropdownVendors = async (): Promise<Vendor[]> => {
    try {
        const response = await axios.get('http://127.0.0.1:8000/listvendor/');
        return response.data; // Pastikan respons sesuai dengan tipe Vendor
    } catch (error) {
        console.error('Error fetching dropdown vendors:', error);
        throw new Error('Failed to fetch dropdown vendors');
    }
};