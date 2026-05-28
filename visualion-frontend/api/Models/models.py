from sqlalchemy import Column, Integer, String, Float, DateTime
from api.database.dbconnections_opt import DatabaseConnection, Base


# Modelos de SQLAlchemy para las tablas de la base de datos

#Productos Tabla de productos disponibles en la óptica, con su SKU, tipo de producto, precio y stock disponible,conectado con vendedor, taller, tecnico y receta médica  

class Producto(Base):
    __tablename__ = "productos"

    sku = Column(String, primary_key=True, index=True)
    tipo_producto = Column(String, index=True)
    precio = Column(Integer)
    stock_disponible = Column(Integer)

    #validaciones estilo setters y getters para cada campo del producto
    

    def __repr__(self):
        return f"<Producto(sku='{self.sku}', tipo_producto='{self.tipo_producto}', precio='{self.precio}', stock_disponible='{self.stock_disponible}')>"



#Receta médica Tabla intermedia entre paciente y medico, con los datos de la receta

class RecetaMedica(Base):
    __tablename__ = "recetas_medicas"

    uuid = Column(String, primary_key=True, index=True)
    paciente_id = Column(String, index=True)
    medico_id = Column(String, index=True)
    fecha_emision = Column(DateTime)
    fecha_vencimiento = Column(DateTime)
    odEsfera = Column(Float)
    odAdicion = Column(Float)
    odCilindro = Column(Float)
    odEje = Column(Float)
    oiEsfera = Column(Float)
    oiAdicion = Column(Float)
    oiCilindro = Column(Float)
    oiEje = Column(Float)
    distancia_pupilar = Column(Float)
    Tipolente = Column(String)


    # Getters y setters para cada campo de la receta médica


    def  __repr__(self):
        return f"<RecetaMedica(uuid='{self.uuid}', paciente_id='{self.paciente_id}', medico_id='{self.medico_id}')>"
    def to_dict(self):
        return {
            "uuid": self.uuid,
            "paciente_id": self.paciente_id,
            "medico_id": self.medico_id,
            "fecha_emision": self.fecha_emision.isoformat() if self.fecha_emision else None,
            "fecha_vencimiento": self.fecha_vencimiento.isoformat() if self.fecha_vencimiento else None,
            "odEsfera": self.odEsfera,
            "odAdicion": self.odAdicion,
            "odCilindro": self.odCilindro,
            "odEje": self.odEje,
            "oiEsfera": self.oiEsfera,
            "oiAdicion": self.oiAdicion,
            "oiCilindro": self.oiCilindro,
            "oiEje": self.oiEje,
            "distancia_pupilar": self.distancia_pupilar,
            "Tipolente": self.Tipolente
        }
    
    
if __name__ == "__main__":
    # Test the database connection and model creation
    try:
        db = DatabaseConnection.get_instance()
        print("Database connection successful!")
        print("Creating tables...")
        Producto.metadata.create_all(bind=DatabaseConnection.engine)
        print("Producto tables created successfully!")
        receta_medica = RecetaMedica.metadata.create_all(bind=DatabaseConnection.engine)
        print("RecetaMedica tables created successfully!")
        DatabaseConnection.Base.metadata.create_all(bind=DatabaseConnection.engine)
        print("Tables created successfully!")
    except Exception as e:
        print(f"Database connection or table creation failed: {e}")

    

