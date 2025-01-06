import axios from 'axios';

export type KeyedObject = {
    [key: string]: string | number | KeyedObject | any;
};

const customers: KeyedObject[] = [];

const fetchCustomers = async () => {
    try {
        const response = await axios.get('http://127.0.0.1:8080/customerdata/');
        const fetchedCustomers = response.data.map((item: any) => ({
            id: item.id || '',
            product: item.name || '',
            date: item.npwp || '',
            status: item.address || '',
            price: item.phone || '',
            rekening: item.bank_account || '',
            add_time: item.add_time || '',
            upd_time: item.upd_time || ''
        }));
        return fetchedCustomers;
    } catch (error) {
        console.error('Error fetching customers from API:', error);
    }
};

const addCustomer = async (newCustomer: KeyedObject) => {
    try {
        await axios.post('http://127.0.0.1:8080/customerdata/', {
            name: newCustomer.product,
            npwp: newCustomer.date,
            address: newCustomer.status,
            phone: newCustomer.price,
            bank_account: newCustomer.rekening,
            add_user: 'admin', 
        });
    } catch (error) {
        console.error('Error adding customer:', error);
    }
};

const updateCustomer = async (updatedCustomer: KeyedObject) => {
    try {
        await axios.put('http://127.0.0.1:8080/customerdata/', {
            id: updatedCustomer.id,
            name: updatedCustomer.product,
            npwp: updatedCustomer.date,
            address: updatedCustomer.status,
            phone: updatedCustomer.price,
            bank_account: updatedCustomer.rekening,
            upd_user: 'admin', 
        });
    } catch (error) {
        console.error('Error updating customer:', error);
    }
};

const deleteCustomer = async (customerId: string) => {
    try {
        await axios.delete('http://127.0.0.1:8080/customerdata/', {
            data: {
                customer_id: customerId,
                upd_user: 'admin', 
            },
        });
    } catch (error) {
        console.error('Error deleting customer:', error);
    }
};


export { fetchCustomers, addCustomer, updateCustomer, deleteCustomer };
