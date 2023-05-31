# Todo-List API Client
# Original created by Thilo Drehlmann
# Modified by Jannik Glane

import requests as r
import os

stillInMenu = True


def clearScreen():
    os.system('clear')


def startUp():
    clearScreen()

    print("Was möchtest du tun?")
    print()
    print("1. Eine neue Liste erstellen")
    print("2. Eine Liste löschen")
    print("3. Eine Liste umbenennen")
    print("4. Einen Eintrag erstellen")
    print("5. Einen Eintrag aktualisieren")
    print("6. Einen Eintrag löschen")
    print("7. Alle Einträge einer Liste anzeigen")
    print("8. Gar nichts")
    print()

    choice = 0

    while True:
        if (choice == "" or not str(choice).isdigit()) or (int(choice) <= 0 or int(choice) >= 9):
            choice = input("Bitte gib eine Zahl ein (1-8): ")
        else:
            if (int(choice) == 8):
                global stillInMenu
                stillInMenu = False
            break

    return int(choice)


def listSelector(prompt):
    clearScreen()
    listLister = r.get("http://127.0.0.1:4200/todo-list")

    i = 0

    if len(listLister.json()) == 0:
        print("Es existiert noch keine Liste")
        print()
        input("Bitte Enter drücken...")
        return False
    else:
        print("Folgende Listen existieren:")
        print()
        while i < len(listLister.json()):
            print("Liste " + str(i+1) + ": " + listLister.json()[i]['name'])
            i += 1
        print()

        choice = 0

        while True:
            if (not str(choice).isdigit()) or (int(choice) <= 0 or int(choice) > len(listLister.json())):

                match prompt:

                    case 'delete': choice = input("Welche Liste möchtest du löschen? (1-"+str(i)+"): ")

                    case 'update': choice = input("Welche Liste möchtest du umbennen? (1-"+str(i)+"): ")

                    case 'create_entry': choice = input("Zu welcher Liste möchtest du einen Eintrag hinzufügen? (1-"+str(i)+"): ")

                    case 'update_entry': choice = input("In welcher Liste möchtest du einen Eintrag aktualisieren? (1-"+str(i)+"): ")

                    case 'delete_entry': choice = input("Aus welcher Liste möchtest du einen Eintrag löschen? (1-"+str(i)+"): ")

                    case 'display_entries': choice = input("Aus welcher Liste möchtest du die Einträge einsehen? (1-"+str(i)+"): ")

            else:
                clearScreen()
                return str(listLister.json()[int(choice)-1]['id'])


def entrySelector(prompt, list_id):
    if list_id is not False:
        clearScreen()
        entryLister = r.get("http://127.0.0.1:4200/todo-list/"+str(list_id))

        i = 0

        if len(entryLister.json()) == 0:
            print("Es existieren noch keine Einträge in dieser Liste")
            print()
            input("Bitte Enter drücken...")
            return False
        else:
            print("Folgende Einträge existieren:")
            print()
            while i < len(entryLister.json()):
                print("Eintrag " + str(i+1) + ": " +
                      entryLister.json()[i]['name'])
                i += 1
            print()

            choice = 0

            while True:
                if (not str(choice).isdigit()) or (int(choice) <= 0 or int(choice) > len(entryLister.json())):

                    match prompt:

                        case 'delete_entry': choice = input("Welchen Eintrag möchtest du löschen? (1-"+str(i)+"): ")

                        case 'update_entry': choice = input("Welchen Eintrag möchtest du aktualisieren? (1-"+str(i)+"): ")

                else:
                    clearScreen()
                    return str(entryLister.json()[int(choice)-1]['id'])
    else:
        return False


def printResult(result, prompt):
    clearScreen()

    match prompt:

        case 'create_list':
            print("Folgende neue Liste wurde angelegt:")
            print()
            print("ID: " + result.json()['id'])
            print("Name: " + result.json()['name'])

        case 'delete_list':
            print("Die Liste wurde erfolgreich gelöscht")

        case 'update_list':
            print("Die Liste sieht nun wie folgt aus: ")
            print()
            print("ID: " + result.json()['id'])
            print("Name: " + result.json()['name'])

        case 'create_entry':
            print("Der folgende Eintrag wurde hinzugefügt:")
            print()
            print("ID: " + result.json()['id'])
            print("Listenreferenz: " + result.json()['list_id'])
            print("Name: " + result.json()['name'])
            print("Beschreibung: " + result.json()['description'])

        case 'update_entry':
            print("Der Eintrag sieht nun wie folgt aus: ")
            print()
            print("ID: " + result.json()['id'])
            print("Listenreferenz: " + result.json()['list_id'])
            print("Name: " + result.json()['name'])
            print("Beschreibung: " + result.json()['description'])

        case 'delete_entry':
            if result.json()['deleted']:
                print("Der Eintrag wurde gelöscht")
            else:
                print("Der Eintrag konnte nicht gelöscht werden")

        case 'display_entries':
            if len(result.json()) >= 1:
                i = 0
                while i < len(result.json()):
                    print("Eintrag " + str(i+1) + ":")
                    print()
                    print("ID: " + result.json()[i]['id'])
                    print("Listenreferenz: " + result.json()[i]['list_id'])
                    print("Name: " + result.json()[i]['name'])
                    print("Beschreibung: " + result.json()[i]['description'])
                    print()
                    i += 1
            else:
                print("Die Liste hat noch keine Einträge")

    print()
    input("Bitte Enter drücken...")


headers = {'Content-type': 'application/json'}

while stillInMenu:

    match startUp():

        case 1:
            clearScreen()
            name = input("Wie soll die neue To-Do Liste heißen? ")
            result = r.post("http://127.0.0.1:4200/todo-list",
                            json={'name': name})
            if (result.status_code == 200):
                printResult(result, 'create_list')
            else:
                print("Fehler beim Schreiben. Wurde kein Name angegeben?")
                print()
                input("Bitte Enter drücken...")
        case 2:
            list_selected = listSelector('delete')

            if list_selected is not False:
                result = r.delete(
                    "http://127.0.0.1:4200/todo-list/" + list_selected)
                if (result.status_code == 200):
                    printResult(result, 'delete_list')
                else:
                    print("Fehler beim Löschen.")
                    print()
                    input("Bitte Enter drücken...")

        case 3:
            list_selected = listSelector('update')

            if list_selected is not False:
                name = input("Wie soll die To-Do Liste heißen? ")
                result = r.patch(
                    "http://127.0.0.1:4200/todo-list/" + list_selected, json={'name': name})
                if (result.status_code == 200):
                    printResult(result, 'update_list')
                else:
                    print("Fehler beim Schreiben. Wurde kein Name angegeben?")
                    print()
                    input("Bitte Enter drücken...")

        case 4:
            list_selected = listSelector('create_entry')
            if list_selected is not False:
                name = input("Wie soll der neue Eintrag heißen? ")
                description = input(
                    "Wie soll die Beschreibung lauten? (darf leer sein): ")
                result = r.post("http://127.0.0.1:4200/todo-list/" + list_selected +
                                "/entry", json={'name': name, 'description': description})
                printResult(result, 'create_entry')

        case 5:
            entry_selected = entrySelector(
                'update_entry', listSelector('update_entry'))

            if entry_selected is not False:
                name = input(
                    "Bitte gib den neuen Namen des Eintrags ein (leer -> alter Name wird beibehalten): ")
                description = input(
                    "Bitte gib die neue Beschreibung des Eintrags ein (leer -> alte Beschreibung wird beibehalten): ")
                result = r.patch("http://127.0.0.1:4200/entry/" + entry_selected,
                                 json={'name': name, 'description': description})
                printResult(result, 'update_entry')

        case 6:
            entry_selected = entrySelector(
                'delete_entry', listSelector('delete_entry'))

            if entry_selected is not False:
                result = r.delete(
                    "http://127.0.0.1:4200/entry/" + entry_selected)
                printResult(result, 'delete_entry')

        case 7:
            list_selected = listSelector('display_entries')

            if list_selected is not False:
                result = r.get(
                    "http://127.0.0.1:4200/todo-list/" + list_selected)
                printResult(result, 'display_entries')
