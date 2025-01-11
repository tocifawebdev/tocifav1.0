import axios from 'axios';
import { fetchDropdownVendors } from '@/_mockApis/apps/supplymanagement/indexListVendor';

export type KeyedObject = {
    [key: string]: string | number | null | undefined | KeyedObject | any;
};

const API_URL = 'http://127.0.0.1:8000/vendoritem/';

// Fetch vendor items
export const fetchVendorItems = async (): Promise<KeyedObject[]> => {
    try {
        const response = await axios.get(API_URL);
        return response.data.map((item: any) => ({
            id: item.VendorItemID || '', // ID unik item
            product: item.ItemName || '', // Nama item
            status: item.Vendor || '', // Nama vendor
            price: item.Price || '', // Harga
            rekening: item.Unit || '', // Satuan
            add_time: item.AddTime || '', // Waktu penambahan
            upd_time: item.UpdTime || '', // Waktu pembaruan
        }));
    } catch (error) {
        console.error('Error fetching vendor items:', error);
        throw new Error('Failed to fetch vendor items');
    }
};

// Add vendor item
export const addVendorItem = async (newVendorItem: KeyedObject): Promise<void> => {
    try {
        const dropdownVendors = await fetchDropdownVendors();
        const selectedVendor = dropdownVendors.find(
            (vendor) => vendor.VendorData === newVendorItem.status // status berisi VendorName
        );

        if (!selectedVendor) {
            throw new Error('Vendor not found in dropdown');
        }

        await axios.post(API_URL, {
            vendordata: selectedVendor.VendorData, // Nama vendor dari dropdown
            itemname: newVendorItem.product, // Nama item
            price: newVendorItem.price, // Harga
            unit: newVendorItem.rekening, // Satuan
            add_user: 'admin', // User yang menambahkan
        });
    } catch (error) {
        console.error('Error adding vendor item:', error);
        throw new Error('Failed to add vendor item');
    }
};

// Update vendor item
export const updateVendorItem = async (updatedVendorItem: KeyedObject): Promise<void> => {
    try {
        const dropdownVendors = await fetchDropdownVendors();
        const selectedVendor = dropdownVendors.find(
            (vendor) => vendor.VendorData === updatedVendorItem.status // status berisi VendorName
        );

        if (!selectedVendor) {
            throw new Error('Vendor not found in dropdown');
        }

        await axios.put(API_URL, {
            itemid: updatedVendorItem.id, // ID unik item
            update_vendordata: selectedVendor.VendorData, // Nama vendor dari dropdown
            update_itemname: updatedVendorItem.product, // Nama item
            update_price: updatedVendorItem.price, // Harga
            update_unit: updatedVendorItem.rekening, // Satuan
            upd_user: 'admin', // User yang memperbarui
        });
    } catch (error) {
        console.error('Error updating vendor item:', error);
        throw new Error('Failed to update vendor item');
    }
};

// Delete vendor item
export const deleteVendorItem = async (vendorItemId: string): Promise<void> => {
    try {
        if (!vendorItemId) {
            throw new Error('Item ID is required');
        }

        console.log('Deleting vendor item with ID:', vendorItemId); // Debugging log
        await axios.delete(API_URL, {
            data: {
                itemid: vendorItemId, // Pastikan nama parameter sesuai dengan backend
                upd_user: 'admin',   // Gunakan user yang valid
            },
        });
    } catch (error) {
        console.error('Error deleting vendor item:', error);
        throw error;
    }
};