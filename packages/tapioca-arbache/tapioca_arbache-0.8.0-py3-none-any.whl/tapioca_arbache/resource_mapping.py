CRM_PERFIL_ENDPOINT = {
    "perfis": {
        "resource": "backend/perfis/",
        "methods": ["GET"],
    }
}
CRM_OAUTH = {
    "oauth_token": {
        "resource": "backend/oauth-token/",
        "methods": ["POST"],
    }
}
CRM_LICENCA_ENDPOINT = {
    "licencas-list": {
        "resource": "/backend/licencas/",
        "methods": ["GET"],
    },
    "licenca": {
        "resource": "/backend/licencas/{codigo}/",
        "methods": ["GET"],
    },
    "licenca_patch": {
        "resource": "/backend/licencas/{codigo}/",
        "methods": ["PATCH"],
    }
}
JOGO_SELF = {
    "jogos": {
        "resource": "/jogos-self/",
        "methods": ["GET"],
    }
}
RELATORIOS = {
    "relatorios": {
        "resource": "/backend/relatorios/",
        "methods": ["GET", "POST"],
    }
}
CRM_JOGO_ENDPOINT = {
    "jogos" : {
        "resource": "/backend/jogos/",
        "methods": ["GET", "POST"]
    },
    "jogo" : {
        "resource": "/backend/jogos/{codigo}/",
        "methods": ["GET", "PATCH"]
    }
}
CRM_EQUIPES_ENDPOINT = {
    "equipes": {
        "resource":"/backend/equipes/",
        "methods": ["GET"],
    },
    "equipe" : {
        "resource": "/backend/equipes/{codigo}/",
        "methods": ["GET"],
    }
}

MIDIAS = {
    "midias": {
        "resource": "/midias/",
        "methods": ["GET"]
    }
}

INTERFACE = {
    "interface": {
        "resource": "/backend/perfis/configuracoes/{codigo}/",
        "methods": ["GET"]
    }
}
