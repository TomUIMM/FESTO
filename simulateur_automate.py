import asyncio 
from asyncua import Server, ua

async def main():
    server = Server()
    await server.init()
    server.set_endpoint("opc.tcp://127.0.0.1:4840") 
    
    # On crée le namespace avec l'index 2 pour correspondre à ton client (ns=2)
    idx = await server.register_namespace("http://festo.simulation")
    obj = server.nodes.objects
    
    # On crée les variables avec des StringNodeIds précis ("s=...")
    trigger = await obj.add_variable(ua.NodeId("Palette_Prete", idx), "Palette_Prete", False)
    c1 = await obj.add_variable(ua.NodeId("Compo_Compartiment_1", idx), "Compo_Compartiment_1", "2R1V2B")
    c2 = await obj.add_variable(ua.NodeId("Compo_Compartiment_2", idx), "Compo_Compartiment_2", "3R3V1B")
    c3 = await obj.add_variable(ua.NodeId("Compo_Compartiment_3", idx), "Compo_Compartiment_3", "1R1V1B")
    
    # Autoriser l'écriture pour pouvoir simuler le changement d'état
    await trigger.set_writable()
    await c1.set_writable()
    await c2.set_writable()
    await c3.set_writable()
    
    print("Faux automate Festo démarré sur opc.tcp://127.0.0.1:4840")
    
    async with server:
        while True:
            # Code de simulation : toutes les 15 secondes, on simule l'arrivée d'une palette
            await asyncio.sleep(10)
            print("\n[Simu] Automate -> Passage de Palette_Prete à TRUE")
            await trigger.set_value(True)
            
            await asyncio.sleep(5)
            await trigger.set_value(False)
            print("[Simu] Automate -> Remise à FALSE du trigger")

if __name__ == "__main__":
    asyncio.run(main())