from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models import Development, Material, User


def seed_if_empty(db: Session) -> None:
    settings = get_settings()

    if not db.execute(select(User).limit(1)).scalar_one_or_none():
        db.add_all(
            [
                User(name="Franco", phone=settings.default_manager_phone or "5500000000000", role="manager", email="franco@evora.local"),
                User(name="Carlos Corretor", phone="5516999999999", role="broker", email="carlos@evora.local"),
                User(name="Ana Corretora", phone="5516888888888", role="broker", email="ana@evora.local"),
            ]
        )
        db.commit()

    if not db.execute(select(Development).limit(1)).scalar_one_or_none():
        developments = [
            Development(
                name="Reserva Évora",
                city="Ribeirão Preto/SP",
                status="ativo",
                description="Loteamento planejado com foco em moradia, infraestrutura e valorização regional.",
                sales_arguments="Localização, infraestrutura, planejamento urbano, potencial de valorização e facilidade de pagamento.",
            ),
            Development(
                name="Jardim Évora",
                city="Sertãozinho/SP",
                status="ativo",
                description="Empreendimento urbano com lotes residenciais e condições acessíveis.",
                sales_arguments="Entrada facilitada, bairro em crescimento e boa relação custo-benefício.",
            ),
            Development(
                name="Terras de Évora",
                city="Interior/SP",
                status="ativo",
                description="Loteamento com perfil de investimento e construção futura.",
                sales_arguments="Potencial de valorização, escassez e escolha antecipada dos melhores lotes.",
            ),
        ]
        db.add_all(developments)
        db.commit()

    if not db.execute(select(Material).limit(1)).scalar_one_or_none():
        reserva = db.execute(select(Development).where(Development.name == "Reserva Évora")).scalar_one_or_none()
        materials = [
            Material(development_id=reserva.id if reserva else None, title="Vídeo aéreo do empreendimento", type="video", url="https://example.com/video-aereo", use_case="Primeiro contato visual", tags="video,aereo,apresentacao"),
            Material(development_id=reserva.id if reserva else None, title="Mapa de localização", type="mapa", url="https://example.com/mapa", use_case="Cliente que não conhece a região", tags="localizacao,mapa,regiao"),
            Material(development_id=reserva.id if reserva else None, title="FAQ documental", type="pdf", url="https://example.com/faq-documental", use_case="Cliente inseguro com documentação", tags="documentacao,seguranca,faq"),
            Material(development_id=reserva.id if reserva else None, title="Argumentos de valorização", type="pdf", url="https://example.com/valorizacao", use_case="Investidor", tags="investidor,valorizacao,liquidez"),
        ]
        db.add_all(materials)
        db.commit()
