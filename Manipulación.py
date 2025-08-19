import os

class Producto:
    """
    Clase que representa un producto en el inventario
    
    Atributos:
        id (str): Identificador único del producto
        nombre (str): Nombre del producto
        cantidad (int): Cantidad en inventario
        precio (float): Precio unitario
    """
    
    def __init__(self, id_producto, nombre, cantidad, precio):
        """Inicializa un nuevo producto"""
        self.id = id_producto
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio
    
    def __str__(self):
        """Representación en cadena del producto"""
        return f"ID: {self.id} | Nombre: {self.nombre} | Cantidad: {self.cantidad} | Precio: ${self.precio:.2f}"


class Inventario:
    """
    Clase que gestiona un inventario de productos
    
    Atributos:
        productos (dict): Diccionario de productos (clave: id_producto)
        archivo (str): Ruta del archivo donde se almacenan los productos
    """
    
    def __init__(self, archivo='inventario.txt'):
        """Inicializa un inventario vacío y carga productos desde un archivo"""
        self.productos = {}
        self.archivo = archivo
        self.cargar_inventario()
    
    def cargar_inventario(self):
        """Carga los productos desde el archivo"""
        if os.path.exists(self.archivo):
            try:
                with open(self.archivo, 'r') as file:
                    for linea in file:
                        id_producto, nombre, cantidad, precio = linea.strip().split('|')
                        self.productos[id_producto] = Producto(id_producto, nombre, int(cantidad), float(precio))
            except (FileNotFoundError, PermissionError) as e:
                print(f"Error al cargar el inventario: {e}")
    
    def guardar_inventario(self):
        """Guarda los productos en el archivo"""
        try:
            with open(self.archivo, 'w') as file:
                for producto in self.productos.values():
                    file.write(f"{producto.id}|{producto.nombre}|{producto.cantidad}|{producto.precio}\n")
        except (PermissionError, IOError) as e:
            print(f"Error al guardar el inventario: {e}")
    
    def agregar_producto(self, producto):
        """Agrega un nuevo producto al inventario"""
        if producto.id in self.productos:
            return False
        self.productos[producto.id] = producto
        self.guardar_inventario()  # Guardar cambios en el archivo
        return True
    
    def eliminar_producto(self, id_producto):
        """Elimina un producto del inventario"""
        if id_producto in self.productos:
            del self.productos[id_producto]
            self.guardar_inventario()  # Guardar cambios en el archivo
            return True
        return False
    
    def actualizar_producto(self, id_producto, cantidad=None, precio=None):
        """Actualiza un producto existente"""
        if id_producto not in self.productos:
            return False
        
        producto = self.productos[id_producto]
        
        if cantidad is not None:
            producto.cantidad = cantidad
        if precio is not None:
            producto.precio = precio
            
        self.guardar_inventario()  # Guardar cambios en el archivo
        return True
    
    def buscar_por_id(self, id_producto):
        """Busca un producto por su ID"""
        return self.productos.get(id_producto)
    
    def buscar_por_nombre(self, nombre_buscado):
        """Busca productos por nombre (búsqueda parcial)"""
        nombre_buscado = nombre_buscado.lower()
        return [p for p in self.productos.values() if nombre_buscado in p.nombre.lower()]
    
    def obtener_todos(self):
        """Obtiene todos los productos del inventario"""
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
