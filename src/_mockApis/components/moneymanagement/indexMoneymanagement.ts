import axios from 'axios';

export type KeyedObject = {
    [key: string]: string | number | null | undefined | KeyedObject | any;
};

const API_URL = 'http://127.0.0.1:8000/moneymanagement/';

export const fetchMoneyManagementItems = async (): Promise<KeyedObject[]> => {
    try {
        const response = await axios.get(API_URL);
        return response.data.map((item: any) => ({
            id: item.ReckID || '',          // Rekening ID
            product: item.BankName || '',   // Bank Name
            status: item.ReckName || '',    // Rekening Name
            price: item.ReckNum || '',  // Rekening Balance
            rekening: item.ReckBalance || '',  // Rekening Nominal
            add_time: item.AddTime || '',   // Waktu Penambahan
            upd_time: item.UpdTime || '',   // Waktu Pembaruan
        }));
    } catch (error) {
        console.error('Error fetching money management items from API:', error);
        throw new Error('Failed to fetch money management items');
    }
};

// Fungsi untuk memperbarui data rekening (UPDATE)
export const updateMoneyManagementItem = async (updatedMoneyManagementItem: KeyedObject): Promise<void> => {
    try {
        await axios.put(API_URL, {
            update_bankname: updatedMoneyManagementItem.product,  // Bank Name
            update_rekname: updatedMoneyManagementItem.status,    // Rekening Name
            update_norek: updatedMoneyManagementItem.price,       // Rekening Balance
            update_nominrek: updatedMoneyManagementItem.rekening, // Rekening Nominal
            rekid: updatedMoneyManagementItem.id,                 // Rekening ID
        });
    } catch (error) {
        console.error('Error updating money management item:', error);
        throw new Error('Failed to update money management item');
    }
};

