import os
import json

class Producto:
    """Clase que representa un producto en el inventario"""
    def __init__(self, id_producto, nombre, cantidad, precio):
        self.id = id_producto
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio
    
    def __str__(self):
        """Representación en cadena del producto"""
        return f"ID: {self.id} | Nombre: {self.nombre} | Cantidad: {self.cantidad} | Precio: ${self.precio:.2f}"

    def to_dict(self):
        """Convierte el producto a diccionario para serialización"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'cantidad': self.cantidad,
            'precio': self.precio
        }

    @classmethod
    def from_dict(cls, data):
        """Crea un producto desde un diccionario"""
        return cls(data['id'], data['nombre'], data['cantidad'], data['precio'])

class Inventario:
    """Clase que gestiona un inventario de productos con persistencia en archivo JSON"""
    
    def __init__(self, archivo='inventario.json'):
        self.archivo = archivo
        self.productos = {}
        self.cargar_inventario()

    def cargar_inventario(self):
        """Carga el inventario desde el archivo con manejo robusto de excepciones"""
        try:
            if os.path.exists(self.archivo):
                with open(self.archivo, 'r') as file:
                    data = json.load(file)
                    self.productos = {k: Producto.from_dict(v) for k, v in data.items()}
        except FileNotFoundError:
            print(f"\nℹ️ Archivo {self.archivo} no encontrado. Se iniciará con inventario vacío.")
        except PermissionError as e:
            print(f"\n❌ Error de permisos: No se puede leer {self.archivo}. Detalle: {str(e)}")
            raise
        except json.JSONDecodeError:
            print(f"\n⚠️ El archivo {self.archivo} está corrupto. Se iniciará con inventario vacío.")
        except Exception as e:
            print(f"\n⚠️ Error inesperado al cargar inventario: {str(e)}")
            self.productos = {}

    def guardar_inventario(self):
        """Guarda el inventario en el archivo con manejo atómico de errores"""
        temp_file = self.archivo + '.tmp'
        try:
            with open(temp_file, 'w') as file:
                json.dump({k: v.to_dict() for k, v in self.productos.items()}, file, indent=4)
            
            # Reemplazo atómico del archivo
            if os.path.exists(self.archivo):
                os.remove(self.archivo)
            os.rename(temp_file, self.archivo)
            
        except PermissionError as e:
            print(f"\n❌ Error de permisos al guardar inventario: {str(e)}")
            if os.path.exists(temp_file):
                os.remove(temp_file)
            raise
        except IOError as e:
            print(f"\n❌ Error de E/S al guardar inventario: {str(e)}")
            if os.path.exists(temp_file):
                os.remove(temp_file)
            raise
        except Exception as e:
            print(f"\n⚠️ Error inesperado al guardar inventario: {str(e)}")
            if os.path.exists(temp_file):
                os.remove(temp_file)
            raise

    # Resto de métodos del inventario...
    def agregar_producto(self, producto):
        try:
            if producto.id in self.productos:
                print(f"\n⚠️ Producto con ID {producto.id} ya existe")
                return False
            self.productos[producto.id] = producto
            self.guardar_inventario()
            return True
        except Exception as e:
            print(f"\n❌ Error al agregar producto: {str(e)}")
            return False

    def eliminar_producto(self, id_producto):
        try:
            if id_producto not in self.productos:
                print(f"\n⚠️ Producto con ID {id_producto} no encontrado")
                return False
            del self.productos[id_producto]
            self.guardar_inventario()
            return True
        except Exception as e:
            print(f"\n❌ Error al eliminar producto: {str(e)}")
            return False

    def actualizar_producto(self, id_producto, cantidad=None, precio=None):
        try:
            if id_producto not in self.productos:
                print(f"\n⚠️ Producto con ID {id_producto} no encontrado")
                return False
            
            producto = self.productos[id_producto]
            if cantidad is not None:
                producto.cantidad = cantidad
            if precio is not None:
                producto.precio = precio
            
            self.guardar_inventario()
            return True
        except Exception as e:
            print(f"\n❌ Error al actualizar producto: {str(e)}")
            return False

    def buscar_por_id(self, id_producto):
        return self.productos.get(id_producto)

    def buscar_por_nombre(self, nombre_buscado):
        nombre_buscado = nombre_buscado.lower()
        return [p for p in self.productos.values() if nombre_buscado in p.nombre.lower()]

    def obtener_todos(self):
        return list(self.productos.values())

def mostrar_menu():
    """Muestra el menú principal"""
    print("\n--- SISTEMA DE GESTIÓN DE INVENTARIO ---")
    print("1. Agregar producto")
    print("2. Eliminar producto")
    print("3. Actualizar producto")
    print("4. Buscar por ID")
    print("5. Buscar por nombre")
    print("6. Mostrar todos los productos")
    print("7. Salir")


def solicitar_datos_producto():
    """Solicita los datos para un nuevo producto"""
    print("\n--- INGRESO DE NUEVO PRODUCTO ---")
    
    # Validar ID
    while True:
        id_producto = input("ID del producto: ").strip()
        if id_producto:
            break
        print("Error: El ID no puede estar vacío")
    
    nombre = input("Nombre del producto: ").strip()
    
    # Validar cantidad
    while True:
        try:
            cantidad = int(input("Cantidad en inventario: "))
            if cantidad >= 0:
                break
            print("Error: La cantidad debe ser 0 o mayor")
        except ValueError:
            print("Error: Debe ingresar un número entero")
    
    # Validar precio
    while True:
        try:
            precio = float(input("Precio unitario: "))
            if precio >= 0:
                break
            print("Error: El precio debe ser 0 o mayor")
        except ValueError:
            print("Error: Debe ingresar un número válido")
    
    return Producto(id_producto, nombre, cantidad, precio)


def main():
    """Función principal del programa"""
    inventario = Inventario()
    
    while True:
        mostrar_menu()
        opcion = input("\nSeleccione una opción (1-7): ")
        
        if opcion == '1':
            producto = solicitar_datos_producto()
            if inventario.agregar_producto(producto):
                print("\n✓ Producto agregado correctamente")
            else:
                print("\n✗ Error: Ya existe un producto con ese ID")
        
        elif opcion == '2':
            id_producto = input("\nIngrese el ID del producto a eliminar: ")
            if inventario.eliminar_producto(id_producto):
                print("\n✓ Producto eliminado correctamente")
            else:
                print("\n✗ Error: No se encontró el producto")
        
        elif opcion == '3':
            id_producto = input("\nIngrese el ID del producto a actualizar: ")
            producto = inventario.buscar_por_id(id_producto)
            
            if producto:
                print(f"\nProducto actual:\n{producto}")
                
                # Obtener nuevos valores (mantener los antiguos si no se ingresan nuevos)
                try:
                    nueva_cantidad = input("Nueva cantidad (deje vacío para mantener): ")
                    cantidad = int(nueva_cantidad) if nueva_cantidad else None
                    
                    nuevo_precio = input("Nuevo precio (deje vacío para mantener): ")
                    precio = float(nuevo_precio) if nuevo_precio else None
                    
                    if inventario.actualizar_producto(id_producto, cantidad, precio):
                        print("\n✓ Producto actualizado correctamente")
                    else:
                        print("\n✗ Error al actualizar el producto")
                except ValueError:
                    print("\n✗ Error: Ingrese valores numéricos válidos")
            else:
                print("\n✗ Error: Producto no encontrado")
        
        elif opcion == '4':
            id_producto = input("\nIngrese el ID del producto a buscar: ")
            producto = inventario.buscar_por_id(id_producto)
            
            if producto:
                print("\nProducto encontrado:")
                print(producto)
            else:
                print("\n✗ Producto no encontrado")
        
        elif opcion == '5':
            nombre = input("\nIngrese el nombre o parte del nombre a buscar: ")
            resultados = inventario.buscar_por_nombre(nombre)
            
            if resultados:
                print(f"\nSe encontraron {len(resultados)} productos:")
                for producto in resultados:
                    print(producto)
            else:
                print("\n✗ No se encontraron productos con ese nombre")
        
        elif opcion == '6':
            productos = inventario.obtener_todos()
            
            if productos:
                print("\n--- LISTADO DE PRODUCTOS ---")
                for producto in productos:
                    print(producto)
                print(f"\nTotal: {len(productos)} productos")
            else:
                print("\nEl inventario está vacío")
        
        elif opcion == '7':
            print("\nSaliendo del sistema...")
            break
        
        else:
            print("\n✗ Opción no válida. Por favor seleccione una opción del 1 al 7.")
        
        input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    main()
