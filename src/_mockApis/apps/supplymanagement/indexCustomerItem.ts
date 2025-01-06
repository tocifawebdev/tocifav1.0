import axios from 'axios';

export type KeyedObject = {
    [key: string]: string | number | null | undefined | KeyedObject | any;
};

const API_URL = 'http://127.0.0.1:8080/customeritem/';

export const fetchCustomerItems = async (): Promise<KeyedObject[]> => {
    try {
        const response = await axios.get(API_URL);
        return response.data.map((item: any) => ({
            id: item.CustomerItemID || '',    // ID item customer
            product: item.ItemName || '',     // Item Name
            status: item.Unit || '',          // Unit masuk ke kolom 'status'
            add_time: item.AddTime || '',     // Waktu penambahan
            upd_time: item.UpdTime || '',     // Waktu pembaruan
        }));
    } catch (error) {
        console.error('Error fetching customer items from API:', error);
        throw new Error('Failed to fetch customer items');
    }
};

export const addCustomerItem = async (newCustomerItem: KeyedObject): Promise<void> => {
    try {
        await axios.post(API_URL, {
            itemname: newCustomerItem.product, // Nama item
            unit: newCustomerItem.status,     // Unit masuk dari kolom 'status'
            add_user: 'admin',                // User yang menambahkan
        });
    } catch (error) {
        console.error('Error adding customer item:', error);
        throw new Error('Failed to add customer item');
    }
};

export const updateCustomerItem = async (updatedCustomerItem: KeyedObject): Promise<void> => {
    try {
        await axios.put(API_URL, {
            itemid: updatedCustomerItem.id,          // ID item customer
            update_itemname: updatedCustomerItem.product, // Item Name diperbarui
            update_unit: updatedCustomerItem.status, // Unit diperbarui dari 'status'
            upd_user: 'admin',                       // User yang memperbarui
        });
    } catch (error) {
        console.error('Error updating customer item:', error);
        throw new Error('Failed to update customer item');
    }
};

export const deleteCustomerItem = async (customerItemId: string): Promise<void> => {
    try {
        await axios.delete(API_URL, {
            data: {
                itemid: customerItemId, // ID item customer yang dihapus
                upd_user: 'admin',      // User yang menghapus
            },
        });
    } catch (error) {
        console.error('Error deleting customer item:', error);
        throw new Error('Failed to delete customer item');
    }
};
