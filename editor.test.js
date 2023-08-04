import { Editor } from './editor'

test('editor renders without crashing', () => {
  const editor = new Editor()
  editor.render()

  expect(editor.node).toBeDefined()
})