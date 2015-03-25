module x10 {
    interface Net {
        void sendMsg(string s);
        string showEnvironment();
        void setActive(string name);
        void setInactive(string name);
        void addModule(string name, string code, string mtype);
        void changeNamebyCode(string name, string code);
        void changeName(string newname, string name);
        bool isActivebyCode(string code);
        bool isAtive(string name);
    };
};


