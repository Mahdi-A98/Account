class Settings(BaseSettings):
    MONGODB_HOST : str
    MONGODB_PORT : str
    MONGODB_DATABASE : str

    AUTH_ACC_KEY1 : str
    AUTH_ACC_KEY2 : str
    AUTH_ACC_KEY3 : str

    ACC_NTF_KEY1 : str
    ACC_NTF_KEY2 : str
    ACC_NTF_KEY3 : str

    ACCOUNT_AUTH_SHARED_KEY : str
    NTF_ACC_SHARED_KEY : str

    AUTHENTICATION_SERVICE_URL : str
    NOTIFICATION_SERVICE_URL : str

    ACC_POD_KEY1 : str
    POD_ACC_SHARED_KEY : str
    
    model_config = SettingsConfigDict(env_file=".env", extra="allow")
