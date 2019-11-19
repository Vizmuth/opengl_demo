import QtQuick 2.0

Rectangle {
    width: 200
    height:200
    color: 'green'
    Text {
        text: 'Hello World'
        anchors.centerIn: parent
    }

    Image {
        id: image
        fillMode: Image.PreserveAspectFit
        anchors.centerIn: root
        source: "./logo.png"
        opacity: 0.5
    }

}
