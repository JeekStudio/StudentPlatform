import {observable, action} from "mobx";
import Provider from '../../../utils/provider';
import {notification} from 'antd';

class SocietyStore {
    @observable loading = false;
    @observable societies = [];
    @observable society = {};

    @observable query = '';

    @action changeLoading() {
        this.loading = !this.loading
    }

    @action changeQuery = (query) => {
        this.query = query;
    };

    @action updateSocietyList = (societies) => {
        this.societies = societies
    };

    @action updateSociety = (society) => {
        this.society = society
    };

    @action fetch = () => {
        this.changeLoading();
        Provider.get('/api/society/')
            .then((res) => {
                this.updateSocietyList(res.data['results']);
                this.changeLoading();
            })
            .catch((err) => {
                this.changeLoading();
                notification.error({
                    message: 'Oops...',
                    description: '获取社团信息失败了，请检查你的网络',
                })
            })
    };

    @action fetchDetail = (id) => {
        this.changeLoading();
        Provider.get(`/api/society/${id}/`)
          .then((res) => {
              this.updateSociety(res.data);
              this.changeLoading();
          })
          .catch((err) => {
              this.changeLoading();
              notification.error({
                  message: 'Oops...',
                  description: '获取社团信息失败了，请检查你的网络',
              })
          })
    };

    @action search = () => {
        this.changeLoading();
        Provider.get('/api/society/', {params: {name: this.query}})
            .then((res) => {
                this.updateSocietyList(res.data['results']);
                this.changeLoading();
            })
            .catch((err) => {
                this.changeLoading();
                notification.error({
                    message: 'Oops...',
                    description: '获取社团信息失败了，请检查你的网络',
                })
            })
    }
}

export default new SocietyStore;
