LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'default': {
            'format': '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',  # INFO уровень в продакшене
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',  # INFO уровень для корневого логгера
    },
    'loggers': {
        'django.db.backends': {
            'level': 'INFO',  # Уровень логирования для баз данных
            'handlers': ['console'],
            'propagate': False,
        },
    },
}
