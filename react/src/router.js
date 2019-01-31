import React from 'react';
import {Route, HashRouter, Switch} from 'react-router-dom';
import Home from './app/home/index.js';
import Society from './app/society/index.js';
import AdminSociety from './app/admin_society/index.js';

// const DEV = process.env.NODE_ENV !== 'production';
// const DEBUG = process.env.DEBUG === 'true';
// const MyRouter = (DEV && !DEBUG) ? HashRouter : BrowserRouter;
const MyRouter = HashRouter;

class AppRouter extends React.Component {
    render() {
        return (
            <MyRouter>
                <div style={{height: '100%'}}>
                    <Switch>
                        <Route path="/society" component={Society}/>
                        <Route path="/admin_society" component={AdminSociety}/>
                        <Route path="" component={Home}/>
                    </Switch>
                </div>
            </MyRouter>
        );
    }
}

export default AppRouter;