app = QApplication(sys.argv)
icon_viewer = IconListViewerWidget()
icon_viewer.setWindowTitle('Icon Viewer')
icon_viewer.show()
icon_viewer.setIconView()
app.exec()