from library import Library




library = Library("books.json", "members.json", "borrowed.json")

while True:
    print("\n1. Add Book")
    print("2. Remove Book")
    print("3. Borrow Book")
    print("4. Renew Borrowed Book")
    print("5. Add Member")
    print("6. Remove Expired Members")
    print("7. Renew Member Subscription")
    print("8. Search Books")
    print("9. Search Members")
    print("10. Comprehensive Report")
    print("11. Quit")
    choice = input("Enter your choice (1-11): ")
    if choice == '1':
        library.add_book()
    elif choice == '2':
        library.remove_book()
    elif choice == '3':
        library.borrow_book()
    elif choice == '4':
        library.renew_borrowed()
    elif choice == '5':
        library.add_member()
    elif choice == '6':
        library.remove_expired_members()
    elif choice == '7':
        library.renew_subscription()
    elif choice == '8':
        library.search_books()
    elif choice == '9':
        library.search_members()
    elif choice == '10':
        library.generate_comprehensive_report()
    elif choice == '11':
        print("Exiting the program.")
        break
    else:
        print("Invalid choice. Please enter a number from 1 to 11.")
