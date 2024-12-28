import axios from 'axios';
export type KeyedObject = {
    [key: string]: string | number | KeyedObject | any;
};

const contacts: KeyedObject[] = []; 

const fetchContacts = async () => {
    try {
        const response = await axios.get('http://127.0.0.1:8080/usermanagement');
        const fetchedContacts = response.data.map((item: any) => ({
            id: item.id || item.UserID, 
            avatar: '', 
            userinfo: item.username || item.Username, 
            usermail: item.email || item.Email,
            phone: item.id || '', 
            jdate: item.add_time || item.AddTime || '', 
            role: item.user_level || item.UserLevel || 'Unknown', 
            password: item.password || item.Password || 'N/A',
            rolestatus: item.user_level === 'Admin' ? 'rgba(255, 0, 0, 0.2)' : 'rgba(0, 128, 0, 0.2)' // Set based on role
        }));
        contacts.splice(0, contacts.length, ...fetchedContacts);
        return fetchedContacts;
    } catch (error) {
        console.error('Error fetching contacts from API:', error);
    }
};

const addContact = async (newContact: KeyedObject) => {
    try {
        await axios.post('http://127.0.0.1:8080/usermanagement/', {
            user_level: newContact.role,
            username: newContact.userinfo,
            password: newContact.password,
            email: newContact.usermail,
            add_user: 'admin'
        });
    } catch (error) {
        console.error('Error adding contact:', error);
    }
};

const updateContact = async (updatedContact: KeyedObject) => {
    try {
        await axios.put('http://127.0.0.1:8080/usermanagement/', {
            username: updatedContact.userinfo,
            user_level: updatedContact.role,
            email: updatedContact.usermail,
            password: updatedContact.password,
            add_user: 'admin'
        });        
    } catch (error) {
        console.error('Error updating contact:', error);
    }
};

const deleteContact = async (username: string) => {
    try {
        await axios.delete('http://127.0.0.1:8080/usermanagement/', {
            data: {
                username,
                add_user: 'admin'
            }
        });
    } catch (error) {
        console.error('Error deleting contact:', error);
    }
};

export { fetchContacts, addContact, updateContact, deleteContact };