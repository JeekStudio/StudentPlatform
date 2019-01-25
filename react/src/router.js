import React from 'react';
import {BrowserRouter, Route, HashRouter, Switch} from 'react-router-dom';
import FormContainer from "./FormContainer";
import Society from './app/society/index.js';
import AdminClub from './app/admin_club/index.js';

const DEV = process.env.NODE_ENV !== 'production';
const DEBUG = process.env.DEBUG === 'true';
const MyRouter = (DEV && !DEBUG) ? HashRouter : BrowserRouter;

class AppRouter extends React.Component {
    render() {
        return (
            <MyRouter>
                <div style={{height: '100%'}}>
                    <Switch>
                        <Route path="/society" component={Society}/>
                        <Route path="/admin_club/" component={AdminClub}/>
                        <Route path="/" component={FormContainer}/>
                    </Switch>
                </div>
            </MyRouter>
        );
    }
}

export default AppRouter;