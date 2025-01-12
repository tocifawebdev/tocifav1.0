import mock from './mockAdapter';

import './apps/chat';
import './apps/supplymanagement';
import './apps/userprofile/posts';
import './apps/userprofile/followers';
import './apps/userprofile/friends';
import './apps/userprofile/gallery';
import './apps/userprofile/photos';
import './apps/blog/index';
import './headerData';
import './apps/notes';
import './apps/requestpo';
import './apps/email';
import './apps/invoice';
import './apps/usermanagement/indexUsermanagement';
import './headerData';
import './apps/kanban';

mock.onAny().passThrough();
