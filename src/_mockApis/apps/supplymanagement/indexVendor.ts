import axios from 'axios';

export type KeyedObject = {
    [key: string]: string | number | null | undefined | KeyedObject | any;
};

export const fetchVendors = async (): Promise<KeyedObject[]> => {
    try {
        const response = await axios.get('http://127.0.0.1:8000/vendordata/');
        return response.data.map((item: any) => ({
            id: item.id || '',
            product: item.name || '',
            status: item.address || '',
            price: item.phone || '',
            rekening: item.bank_account || '',
            add_time: item.add_time || '',
            upd_time: item.upd_time || ''
        }));
    } catch (error) {
        console.error('Error fetching vendors from API:', error);
        return [];
    }
};

export const addVendor = async (newVendor: KeyedObject) => {
    try {
        await axios.post('http://127.0.0.1:8000/vendordata/', {
            name: newVendor.product,
            address: newVendor.status,
            phone: newVendor.price,
            bank_account: newVendor.rekening,
            add_user: 'yosephatigoran', 
        });
    } catch (error) {
        console.error('Error adding vendor:', error);
    }
};

export const updateVendor = async (updatedVendor: KeyedObject) => {
    try {
        await axios.put('http://127.0.0.1:8000/vendordata/', {
            vendor_id: updatedVendor.id,
            name: updatedVendor.product,
            address: updatedVendor.status,
            phone: updatedVendor.price,
            bank_account: updatedVendor.rekening,
            upd_user: 'yosephatigoran',
        });
    } catch (error) {
        console.error('Error updating vendor:', error);
    }
};

export const deleteVendor = async (vendorId: string) => {
    try {
        await axios.delete('http://127.0.0.1:8000/vendordata/', {
            data: {
                vendor_id: vendorId,
                upd_user: 'yosephatigoran',
            },
        });
    } catch (error) {
        console.error('Error deleting vendor:', error);
    }
};
