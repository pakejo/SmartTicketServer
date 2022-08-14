// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.4;

contract Purchase {
    // Event price
    uint public price;
    // Promoter address
    address payable public seller;
    // Promoter UID
    string private promoter_uid;
    // Event ID
    string private event_id;
    // Customer ID
    string private customer_id;
    // Customer address
    address payable public buyer;
    // Possibles states of the contract
    enum State { Created, Locked, Release, Inactive }
    // The state variable has a default value of the first member, `State.created`
    State public state;

    /* POSSIBLE CONTRACT ERRORS */

    // Only the buyer can call this function.
    error OnlyBuyer();
    // Only the seller can call this function.
    error OnlySeller();
    // The function cannot be called at the current state.
    error InvalidState();

    /* CONTRACT MODIFIERS */

    modifier onlyBuyer() {
        if (msg.sender != buyer)
            revert OnlyBuyer();
        _;
    }

    modifier onlySeller() {
        if (msg.sender != seller)
            revert OnlySeller();
        _;
    }

    modifier inState(State state_) {
        if (state != state_)
            revert InvalidState();
        _;
    }


    /* EVENTS EMITTED BY THE CONTRACT */
    event PurchaseConfirmed();
    event ItemReceived();
    event SellerRefunded();

    // Promoter address comes with the message
    constructor(uint _price, string memory _promoter_uid, string memory _event_id, string memory _customer_id) payable {
        price = _price;
        seller = payable(msg.sender);
        promoter_uid = _promoter_uid;
        event_id = _event_id;
        customer_id = _customer_id;
    }

    /// Confirm the purchase as buyer.
    /// The ether will be locked until confirmReceived
    /// is called.
    function confirmPurchase()
        external
        payable
        inState(State.Created)
    {
        emit PurchaseConfirmed();
        buyer = payable(msg.sender);
        price = msg.value;
        state = State.Locked;
    }

    /// Confirm that you (the buyer) received the item.
    /// This will release the locked ether.
    function confirmReceived()
        external
        onlyBuyer
        inState(State.Locked)
    {
        emit ItemReceived();
        // It is important to change the state first because
        // otherwise, the contracts called using `send` below
        // can call in again here.
        state = State.Release;
    }

    /// This function refunds the seller, i.e.
    /// pays back the locked funds of the seller.
    function refundSeller()
        external
        payable
        onlySeller
        inState(State.Release)
    {
        emit SellerRefunded();
        state = State.Inactive;
        seller.transfer(price);
    }
}